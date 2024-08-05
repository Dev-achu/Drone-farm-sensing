import numpy as np
import cv2

def calculate_ndvi(infrared_image_path, red_band_image_path):
    # Read infrared and red band images
    infrared_image = cv2.imread(infrared_image_path, cv2.IMREAD_GRAYSCALE).astype(np.float32)
    red_band_image = cv2.imread(red_band_image_path, cv2.IMREAD_GRAYSCALE).astype(np.float32)

    # Resize the images to have the same dimensions
    red_band_image = cv2.resize(red_band_image, (infrared_image.shape[1], infrared_image.shape[0]))

    # Avoid division by zero
    ndvi_denominator = infrared_image + red_band_image
    ndvi_denominator[ndvi_denominator == 0] = 1

    # Calculate NDVI
    ndvi = (infrared_image - red_band_image) / ndvi_denominator

    # Calculate the mean NDVI value
    mean_ndvi = np.mean(ndvi)

    return mean_ndvi

def categorize_ndvi(ndvi_value):
    ndvi_value = float(ndvi_value)
    if ndvi_value < 0:
        return "Non-vegetated (Water, Bare Soil, Urban)"
    elif ndvi_value == 0:
        return "Barren (Little or No Vegetation)"
    elif 0 < ndvi_value <= 0.2:
        return "Sparse or Stressed Vegetation"
    elif 0.2 < ndvi_value <= 0.5:
        return "Moderate Vegetation (Reasonably Healthy)"
    elif 0.5 < ndvi_value <= 1:
        return "Lush, Healthy Vegetation (High Biomass)"
    else:
        return "Invalid NDVI Value"

def calculate_aqi(pm25, pm10):
    def calculate_aqi_individual(pm_value, breakpoints, c_low, c_high, i_low, i_high):
        if pm_value <= breakpoints[0]:
            aqi = ((i_high - i_low) / (c_high - c_low)) * (pm_value - c_low) + i_low
            return round(aqi)
        for i in range(1, len(breakpoints)):
            if pm_value <= breakpoints[i]:
                aqi = ((i_high - i_low) / (breakpoints[i] - breakpoints[i - 1])) * (pm_value - breakpoints[i - 1]) + i_low
                return round(aqi)
        aqi = ((i_high - i_low) / (c_high - breakpoints[-1])) * (pm_value - breakpoints[-1]) + i_low
        return round(aqi)

    def calculate_aqi_pm25(pm25_value):
        breakpoints = [12.0, 35.4, 55.4, 150.4, 250.4]
        return calculate_aqi_individual(pm25_value, breakpoints, 0, 250.4, 0, 300)

    def calculate_aqi_pm10(pm10_value):
        breakpoints = [54.0, 154.0, 254.0, 354.0, 424.0]
        return calculate_aqi_individual(pm10_value, breakpoints, 0, 424.0, 0, 300)

    aqi_pm25 = calculate_aqi_pm25(pm25)
    aqi_pm10 = calculate_aqi_pm10(pm10)

    return max(aqi_pm25, aqi_pm10)

def categorize_soil_quality(ph_value):
    if 6.5 <= ph_value <= 7.5:
        return "Neutral soil, perfect!"
    elif 6.0 <= ph_value < 6.5:
        return "Slightly acidic soil, somewhat optimal for plants"
    elif 7.5 < ph_value <= 8.0:
        return "Slightly alkaline, somewhat optimal for plants"
    elif ph_value < 6.0:
        return "Acidic, please add some more alkali"
    elif ph_value > 8.0:
        return "Alkaline, please add some more acid"
    else:
        return "Invalid pH value"

# Example usage for NDVI calculation
infrared_image_path = 'infrared_image.tif'
red_band_image_path = 'red_img.tif'

mean_ndvi_result = calculate_ndvi(infrared_image_path, red_band_image_path)

# You can now use mean_ndvi_result for further analysis or print it
value = mean_ndvi_result
print("Your NDVI value is:", round(mean_ndvi_result, 2))
print(categorize_ndvi(value))

# Example usage for AQI calculation
try:
    pm25_value = float(input("Enter PM2.5 value (µg/m³): "))
    pm10_value = float(input("Enter PM10 value (µg/m³): "))

    result_aqi = calculate_aqi(pm25_value, pm10_value)
    print(f"The Air Quality Index (AQI) is: {result_aqi}")
except ValueError:
    print("Invalid input. Please enter numeric values for PM2.5 and PM10.")

# Example usage for soil quality categorization
try:
    ph_input = float(input("Enter the soil pH value: "))
    result = categorize_soil_quality(ph_input)
    print(f"The soil quality is {result}")
except ValueError:
    print("Invalid input. Please enter a numeric value for pH.")