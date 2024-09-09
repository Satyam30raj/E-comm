from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Data structure for fertilizers with pricing
fertilizer_data = {
    'Urea': {
        'nutrient': 'Nitrogen',
        'price_per_kg': 20  # price in local currency per kg
    },
    'DAP': {
        'nutrient': 'Nitrogen and Phosphorus',
        'price_per_kg': 30  # price in local currency per kg
    },
    'MOP': {
        'nutrient': 'Potassium',
        'price_per_kg': 25  # price in local currency per kg
    },
    'NPK': {
        'nutrient': 'Nitrogen, Phosphorus, Potassium',
        'price_per_kg': 40  # price in local currency per kg
    }
}

# Example crop and nutrient data
crop_data = {
    'Wheat': {
        'nutrients': {'nitrogen': 120, 'phosphorus': 60, 'potassium': 40},
        'temperature': {'min': 10, 'max': 25},
        'area': {'min': 0.25, 'max': 10.0}  # area in acres
    },
    'Rice': {
        'nutrients': {'nitrogen': 150, 'phosphorus': 70, 'potassium': 50},
        'temperature': {'min': 20, 'max': 35},
        'area': {'min': 0.12, 'max': 5.0}  # area in acres
    },
    'Corn': {
        'nutrients': {'nitrogen': 180, 'phosphorus': 80, 'potassium': 60},
        'temperature': {'min': 15, 'max': 30},
        'area': {'min': 0.5, 'max': 10.0}  # area in acres
    }
}


# Function to get fertilizer recommendations based on user inputs
def get_fertilizer_recommendation(crop_name, temp, area, soil_nutrients):
    crop = crop_data.get(crop_name)

    if crop:
        crop_nutrients = crop['nutrients']
        temp_range = crop['temperature']
        area_range = crop['area']

        # Check if temperature and area are within the recommended ranges
        temp_ok = temp_range['min'] <= temp <= temp_range['max']
        area_ok = area_range['min'] <= area <= area_range['max']

        # Calculate nutrient deficiencies
        deficiencies = {}
        for nutrient, required_amount in crop_nutrients.items():
            current_amount = soil_nutrients.get(nutrient, 0)
            if current_amount < required_amount:
                deficiencies[nutrient] = required_amount - current_amount

        recommendations = {}
        for nutrient, deficiency in deficiencies.items():
            for fert, info in fertilizer_data.items():
                if info['nutrient'].lower() == nutrient:
                    # Calculate amount of fertilizer needed based on deficiency
                    quantity_needed = deficiency
                    # Calculate cost based on quantity and price per kg
                    cost = quantity_needed * info['price_per_kg']
                    recommendations[fert] = {
                        'quantity_needed': quantity_needed,
                        'cost': cost
                    }
                    break

        if temp_ok and area_ok:
            return {
                'nutrients': crop_nutrients,
                'temperature': f"{temp_range['min']} - {temp_range['max']} °C",
                'area': f"{area_range['min']} - {area_range['max']} acres",
                'recommendations': recommendations
            }
        else:
            return {'error': 'Temperature or area not within the recommended range.'}
    else:
        return {'error': 'Crop not found.'}




@app.route('/')
def home():
    return render_template('home.html')




@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    crop_type = request.form.get('crop_type')
    temperature = float(request.form.get('temperature'))
    area = float(request.form.get('area'))  # Area in acres

    # Get soil nutrients data from the form
    soil_nutrients = {
        'nitrogen': float(request.form.get('nitrogen')),
        'phosphorus': float(request.form.get('phosphorus')),
        'potassium': float(request.form.get('potassium'))
    }

    recommendations = get_fertilizer_recommendation(crop_type, temperature, area, soil_nutrients)

    if 'error' in recommendations:
        return jsonify(recommendations), 400
    else:
        return jsonify({
            'crop': crop_type,
            'recommendation': recommendations
        })



