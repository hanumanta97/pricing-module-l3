from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from .models import (
    PricingConfiguration,
    DistanceBasePrice,
    DistanceAdditionalPrice,
    TimeMultiplierFactor,
    WaitingCharge
)

def home(request):
    return render(request, 'pricing/home.html')

@csrf_exempt
def simple_calculate_price(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)

        ride_date = data.get('date')
        total_distance_km = float(data.get('total_distance_km', 0))
        total_time_minutes = int(data.get('total_time_minutes', 0))
        wait_time_minutes = int(data.get('wait_time_minutes', 0))
        print(ride_date,total_distance_km,total_time_minutes,wait_time_minutes)

        ride_day_code = datetime.datetime.strptime(ride_date, '%Y-%m-%d').strftime('%a').lower()[:3]

        # Manually filter JSONField
        config = next(
            (cfg for cfg in PricingConfiguration.objects.filter(is_active=True)
             if ride_day_code in cfg.applicable_days),
            None
        )

        if not config:
            return JsonResponse({'error': 'No active config for that day'}, status=404)

        # 1. Base Price (DBP)
        dbp_entry = DistanceBasePrice.objects.filter(config=config).order_by('-base_km').first()
        base_km = dbp_entry.base_km if dbp_entry else 0
        DBP = dbp_entry.price if dbp_entry else 0

        # 2. Additional Distance Price (Dn * DAP)
        Dn = max(total_distance_km - base_km, 0)
        dap_entry = DistanceAdditionalPrice.objects.filter(config=config).first()
        DAP = dap_entry.price_per_km if dap_entry else 0
        additional_distance_price = Dn * DAP

        # 3. Time-based Charge (Tn * TMF)
        Tn = total_time_minutes
        tmf_entries = TimeMultiplierFactor.objects.filter(config=config).order_by('from_minute')
        TMF = 1
        for tmf in tmf_entries:
            if tmf.from_minute <= Tn <= tmf.to_minute:
                TMF = tmf.multiplier
                break
        time_price = (Tn / 60) * 100 * TMF  # 100 is base hourly rate

        # 4. Waiting Charge (WC)
        wc_entry = WaitingCharge.objects.filter(config=config).first()
        WC = 0
        if wc_entry and wait_time_minutes > wc_entry.grace_period_minutes:
            extra_wait = wait_time_minutes - wc_entry.grace_period_minutes
            WC = (extra_wait / wc_entry.unit_minutes) * wc_entry.charge_per_unit

        # Total Price Calculation
        total_price = round(DBP + additional_distance_price + time_price + WC, 2)

        return JsonResponse({
            "formula": "$Price = (DBP + (Dn × DAP)) + (Tn × TMF) + WC$",
            "DBP": round(DBP, 2),
            "Dn": round(Dn, 2),
            "DAP": round(DAP, 2),
            "DistancePrice": round(DBP + additional_distance_price, 2),
            "Tn": Tn,
            "TMF": TMF,
            "TimePrice": round(time_price, 2),
            "WC": round(WC, 2),
            "TotalPrice": total_price
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
