
def my_function(id):
    return "Hello from a function"

keyD={
    "nw":{ #network
        "branding":"netw_branding",
        "createdAt":"netw_created",
        "created_at":"netw_created",
        "description":"netw_description",
        "name":"netw_name",
        "_id":"netw_id",
    },
    "syst":{
        "_id":"id",
        "name":"name",
        "serial":"serial",
        "type":"type",
        "city":"local",
        "created_at":"created",
        "latitude":"lat_",
        "longitude":"lon_",
        "network":"netw_id",
#        "networkName":"netw_name",
	    "networks":"netw_id",
        "lastRequest":{
            "date":"lastLinkDt",
            "ip":"ip",
        } 
    },
    "sensors":{
	"date":"dt",
    },
    "ipma":{
        "date":"dt",
        "humidade":"rh",
        "idDireccVento":"wd",
        "intensidadeVento":"ws",
        "intensidadeVentoKM":"wskm",
        "precAcumulada":"ra",
        "pressao":"ap",
        "radiacao":"sun",
        "temperatura":"at",
        "staID":"id",
        "dt":"dt",
        "rh":"rh",
        "wd":"wd",
        "ws":"ws",
        "wskm":"wskm",
        "ra":"ra",
        "ap":"ap",
        "sun":"sun",
        "at":"at",
        "id":"id",
    },
    "ipmasys":{
#       "type":"type",
        "geometry":{
            "coordinates":{
                "0":"lat_",
                "1":"lon_",
            }
        },
        "properties":{
            "idEstacao": "id",
            "localEstacao":"local",
        }
    },
    "qualar":{ #valores tal como vem do qualar
        "PM2.5":6001,
        "O3":7,
        "PM10":5,
        "NO2":8,
        "SO2":1,
        "CO":10,
        "C6H6":20,
        "NOx":9,
        "NO":38, #estação de Aveiro por exculoção de partes
        "As in PM10":42,
        "BaP in PM10":44,
        "Cd in PM10":41,
        "Ni in PM10":40,
        "Pb in PM10":39,
        "ID21":21,
        "ID431":431,
        "ID464":464,
        "ID482":482
    },
    "qualarsens":{
        "valor":"valor",
        "data":"dt"
    },
    "qualarid":{  #nome ja modificados do qualar
        "6001":"pm25",
        "7":"o3",
        "5":"pm10",
        "8":"no2",
        "1":"so2",
        "10":"co",
        "20":"c6h6",
        "9":"nox",
        "38":"no",
        "42":"pm10as",
        "44":"pm10bap",
        "41":"pm10cd",
        "40":"pm10ni",
        "39":"pm10pb",
        "21":"id21",
        "431":"id431",
        "464":"id464",
        "482":"id482"
    },
    "qualarSenseName":{  #correspondencia de nomes
        "PM2.5":"pm25",
        "O3":"o3",
        "PM10":"pm10",
        "NO2":"no2",
        "SO2":"so2",
        "CO":"co",
        "C6H6":"c6h6",
        "NOx":"nox",
        "NO":"no",
        "As in PM10":"pm10as",
        "BaP in PM10":"pm10bap",
        "Cd in PM10":"pm10cd",
        "Ni in PM10":"pm10ni",
        "Pb in PM10":"pm10pb",
        "ID21":"id21",
        "ID431":"id431",
        "ID464":"id464",
        "ID482":"id482"
    },
    "qualarsys":{
        "features":{
            "attributes":{
                "estacao_id": "id",
                "estacao_nome":"local",
                "poluente_abv":"sensors"
            },
            "geometry":{
                "x":"lat_",
                "y":"lon_"
            }
        }
    },
    "server":{
        "api":{
            "monitar":"monitarBot.py",
            "qualar":"qualarBot.py"
        }
    },
    "poluents":{'db': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level'}, 'sun': {'unit': 'w/m&#178;', 'chart': 'line', 'icon': 'wi-day-sunny', 'legend': 'Radiation (W/m2)', 'type': 'Global Solar Radiation'}, 'wl': {'unit': 'm', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Water Level (Meters)', 'type': 'Water Level'}, 'wt': {'unit': 'ºC', 'chart': 'line', 'icon': 'fa-thermometer', 'legend': 'Temperature (ºC)', 'type': 'Water Temperature'}, 'at': {'unit': 'ºC', 'chart': 'line', 'icon': 'wi-thermometer', 'legend': 'Temperature (ºC)', 'type': 'Air Temperature'}, 'ap': {'unit': 'hPa', 'chart': 'line', 'icon': 'wi-barometer', 'legend': 'Pressure (hPa) ', 'type': 'Atmospheric Pressure'}, 'co2': {'unit': 'ppm', 'chart': 'line', 'icon': 'CO&#8322;', 'legend': ' Concentration (ppm)', 'type': 'Carbon Dioxide'}, 'co2mv': {'unit': 'mV', 'chart': 'line', 'icon': 'CO&#8322; mV', 'legend': ' Concentration (mV)', 'type': 'Carbon Dioxide - mV'}, 'co': {'unit': '&#181;g/m&#179;', 'chart': 'line', 'icon': 'CO', 'legend': ' Concentration (μg/m3)', 'type': 'Carbon Monoxide'}, 'tc': {'unit': 'ºC', 'chart': 'line', 'icon': 'T_C', 'legend': 'Temperature (ºC)', 'type': 'Controller Temperature'}, 'wsm': {'unit': 'km/h', 'chart': 'line', 'icon': 'Vmx', 'legend': 'Speed (km/h)', 'type': 'Maximum Wind Speed'}, 'no2': {'unit': '&#181;g/m&#179;', 'chart': 'line', 'icon': 'NO&#8322;', 'legend': 'Concentration (μg/m3)', 'type': 'Nitrogen Dioxide'}, 'no2mv': {'unit': 'mV', 'chart': 'line', 'icon': 'NO&#8322;mV', 'legend': 'Concentration (mV)', 'type': 'Nitrogen Dioxide - mV'}, 'oxmv': {'unit': 'mV', 'chart': 'line', 'icon': 'Ox mV', 'legend': 'Concentration (mV)', 'type': 'Oxidising Substances - mV'}, 'ox': {'unit': '&#181;g/m&#179;', 'chart': 'line', 'icon': 'Ox', 'legend': 'Concentration (μg/m3)', 'type': 'Oxidising Substances (O3 + NO2)'}, 'o3': {'unit': '&#181;g/m&#179;', 'chart': 'line', 'icon': 'O&#8323;', 'legend': 'Concentration (μg/m3)', 'type': 'Ozone'}, 'pm1': {'unit': '&#181;g/m&#179;', 'chart': 'line', 'icon': 'PM 1', 'legend': 'Concentração (μg/m3)', 'type': 'PM 1'}, 'pm10': {'unit': '&#181;g/m&#179;', 'chart': 'line', 'icon': 'PM 10', 'legend': 'Concentração (μg/m3)', 'type': 'PM 10'}, 'pm25': {'unit': '&#181;g/m&#179;', 'chart': 'line', 'icon': 'PM 2.5', 'legend': 'Concentração (μg/m3)', 'type': 'PM 2.5'}, 'ra': {'unit': 'mm', 'chart': 'column', 'icon': 'wi-rain', 'legend': 'Precipitation (mm/time interval) ', 'type': 'Precipitation'}, 'rh': {'unit': '%', 'chart': 'line', 'icon': 'wi-humidity', 'legend': 'Relative Humidity (%)', 'type': 'Relative Humidity'}, 'so2': {'unit': '&#181;g/m&#179;', 'chart': 'line', 'icon': 'SO&#8322;', 'legend': 'Concentration (μg/m3)', 'type': 'Sulfur Dioxide'}, 'so2mv': {'unit': 'mV', 'chart': 'line', 'icon': 'SO&#8322; mV', 'legend': 'Concentration (mv)', 'type': 'Sulfur Dioxide - mv'}, 'iuv': {'unit': 'UV', 'chart': 'line', 'icon': 'wi-hot', 'legend': ' Ultraviolet Index (uv)', 'type': 'Ultraviolet Index'}, 'wd': {'unit': 'º', 'chart': 'line', 'icon': 'wi-wind-direction', 'legend': 'Direction (º)', 'type': 'Wind Direction'}, 'ws': {'unit': 'km/h', 'chart': 'line', 'icon': 'wi-strong-wind', 'legend': 'Speed (km/h)', 'type': 'Wind Speed'}, 'comv': {'unit': 'mV', 'chart': 'line', 'icon': 'CO&#8322; mV', 'legend': 'Concentration (mV)', 'type': 'Carbon Monoxide - mV'}, 'voc': {'unit': '&#181;g/m&#179;', 'chart': 'line', 'icon': 'VOC', 'legend': 'Concentration (ppm) ', 'type': 'Volatile Organic Compounds'}, 'ph': {'unit': 'u', 'chart': 'line', 'icon': 'PH', 'legend': 'PH ', 'type': 'Water PH'}, 'wtmv': {'unit': 'mV', 'chart': 'line', 'icon': 'WT mV', 'legend': 'Temperatura da Agua mV', 'type': 'Temperatura da Água - mV'}, 'phmv': {'unit': 'mV', 'chart': 'line', 'icon': 'PH mV', 'legend': 'PH_mv', 'type': 'PH - mV'}, 'so2amv': {'unit': 'mV', 'chart': 'line', 'icon': 'SO&#8322; mV', 'legend': 'Concentração AUX (mV)', 'type': 'Dióxido de Enxofre Aux - mV'}, 'no2amv': {'unit': 'mV', 'chart': 'line', 'icon': 'NO&#8322;mV', 'legend': 'Concentration (mV)', 'type': 'Nitrogen Dioxide Aux - mV'}, 'coamv': {'unit': 'mV', 'chart': 'line', 'icon': 'COAMV', 'legend': 'Concentration (mV)', 'type': 'Carbon Monoxide Aux - mV'}, 'oxamv': {'unit': 'mV', 'chart': 'line', 'icon': 'OxAmV', 'legend': 'Concentration (mV)', 'type': 'Oxidising Substances Aux - mV'}, 'bat': {'unit': '%', 'chart': 'line', 'icon': 'fa-battery-full', 'legend': 'Battery (%)', 'type': 'Battery'}, 'flwp': {'unit': 'l/m', 'chart': 'line', 'icon': 'flwp', 'legend': 'Air Flow (l/m)', 'type': 'Air Flow PMs'}, 'flwa': {'unit': 'l/m', 'chart': 'line', 'icon': 'flwa', 'legend': 'Air Flow (l/m)', 'type': 'Air Flow Poluents'}, 'sm1': {'unit': '%', 'chart': 'line', 'icon': 'SM1', 'legend': 'Soil Moisture 1', 'type': 'Soil Moisture 1'}, 'sm2': {'unit': '%', 'chart': 'line', 'icon': 'SM2', 'legend': 'Soil Moisture 2', 'type': 'Soil Moisture 2'}, 'sm3': {'unit': '%', 'chart': 'line', 'icon': 'SM3', 'legend': 'Soil Moisture 3', 'type': 'Soil Moisture 3'}, 'lw': {'unit': 'u', 'chart': 'line', 'icon': 'fa-leaf', 'legend': 'Wetness (u)', 'type': 'Leaf Wetness'}, 'sm1mv': {'unit': 'mV', 'chart': 'line', 'icon': 'SM1 mV', 'legend': 'Soil Moisture 1 milivolts', 'type': 'Soil Moisture 1 milivolts'}, 'sm2mv': {'unit': 'mV', 'chart': 'line', 'icon': 'SM2 mV', 'legend': 'Soil Moisture 2 milivolts', 'type': 'Soil Moisture 2 milivolts'}, 'sm3mv': {'unit': 'mV', 'chart': 'line', 'icon': 'SM3 mV', 'legend': 'Soil Moisture 3 milivolts', 'type': 'Soil Moisture 3 milivolts'}, 'lwmv': {'unit': 'mV', 'chart': 'line', 'icon': 'lw mV', 'legend': 'Leaf Wetness milivolts', 'type': 'Leaf Wetness milivolts'}, 'ec': {'unit': 'µS/cm', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Electrical Conductivity ', 'type': 'Water Electrical Conductivity '}, 'ecmv': {'unit': 'mV', 'chart': 'line', 'icon': 'EC mV', 'legend': 'Electrical Conductivity milivolts', 'type': 'Electrical Conductivity miliVolts'}, 'st': {'unit': 'ºC', 'chart': 'line', 'icon': 'fa-thermometer', 'legend': 'Temperature (ºC)', 'type': 'Soil Temperature'}, 'stmv': {'unit': 'mV', 'chart': 'line', 'icon': 'fa-thermometer', 'legend': 'Soil Temperature milivolts', 'type': 'Soil Temperature milivolts'}, 'wlmv': {'unit': 'mV', 'chart': 'line', 'icon': 'wlmv', 'legend': 'Water Level - milivolts', 'type': 'Water Level mV'}, 'zled': {'unit': 'u', 'chart': 'line', 'icon': 'wi-barometer', 'legend': ' ', 'type': 'zled'}, 'zconf': {'unit': 'u', 'chart': 'column', 'icon': 'mi_build', 'legend': ' ', 'type': 'Settings'}, 'd1c1': {'unit': 'u', 'chart': 'column', 'icon': 'fa-motorcycle', 'legend': 'Traffic Count', 'type': 'Traffic Counter Direction 1 Class 1'}, 'd1c2': {'unit': 'u', 'chart': 'column', 'icon': 'fa-car-side', 'legend': 'Traffic Count', 'type': 'Traffic Counter Direction 1 Class 2'}, 'd1c3': {'unit': 'u', 'chart': 'column', 'icon': 'fa-shuttle-van', 'legend': 'Traffic Count', 'type': 'Traffic Counter Direction 1 Class 3'}, 'd1c4': {'unit': 'u', 'chart': 'column', 'icon': 'fa-truck', 'legend': 'Traffic Count', 'type': 'Traffic Counter Direction 1 Class 4'}, 'd1c5': {'unit': 'u', 'chart': 'column', 'icon': 'fa-truck-moving', 'legend': 'Traffic Count', 'type': 'Traffic Counter Direction 1 Class 5'}, 'd2c1': {'unit': 'u', 'chart': 'column', 'icon': 'fa-motorcycle', 'legend': 'Traffic Count', 'type': 'Traffic Counter Direction 2 Class 1'}, 'd2c2': {'unit': 'u', 'chart': 'column', 'icon': 'fa-car-side', 'legend': 'Traffic Count', 'type': 'Traffic Counter Direction 2 Class 2'}, 'd2c3': {'unit': 'u', 'chart': 'column', 'icon': 'fa-shuttle-van', 'legend': 'Traffic Count', 'type': 'Traffic Counter Direction 2 Class 3'}, 'd2c4': {'unit': 'u', 'chart': 'column', 'icon': 'fa-truck', 'legend': 'Traffic Count', 'type': 'Traffic Counter Direction 2 Class 4'}, 'd2c5': {'unit': 'u', 'chart': 'column', 'icon': 'fa-truck-moving', 'legend': 'Traffic Count', 'type': 'Traffic Counter Direction 2 Class 5'}, 'tsma': {'unit': 'km/h', 'chart': 'column', 'icon': 'TSmax', 'legend': 'Traffic Speed Km/h', 'type': 'Traffic Speed Max'}, 'tsmi': {'unit': 'km/h', 'chart': 'column', 'icon': 'TSmin', 'legend': 'Traffic Speed Km/h', 'type': 'Traffic Speed Min'}, 'tsa': {'unit': 'km/h', 'chart': 'column', 'icon': 'TSavg', 'legend': 'Traffic Speed Km/h', 'type': 'Traffic Speed Avg'}, 'pos_x': {'unit': 'u', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Maximum Acceleration in X', 'type': 'Maximum Acceleration in X'}, 'pos_y': {'unit': 'u', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Maximum Acceleration in Y', 'type': 'Maximum Acceleration in Y'}, 'pos_z': {'unit': 'u', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Maximum Acceleration in Z', 'type': 'Maximum Acceleration in Z'}, 'turb': {'unit': 'NTU', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Water Turbidity', 'type': 'Water Turbidity'}, 'orp': {'unit': 'mV', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Water Oxidation Reduction Potential', 'type': 'Water Oxidation Reduction Potential '}, 'sal': {'unit': 'PSU', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Water Salinity', 'type': 'Water Salinity'}, 'dox': {'unit': 'mg/L', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Water Dissolved Oxygen', 'type': 'Water Dissolved Oxygen'}, 'doxp': {'unit': '%', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Dissolved Oxygen % Air Saturation', 'type': 'Water Dissolved Oxygen Air Saturation'}, 'ec20': {'unit': 'µS/cm', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Electrical Conductivity 20 Dreg', 'type': 'Water Electrical Conductivity 20 Dreg'}, 'ec25': {'unit': 'µS/cm', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Electrical Conductivity 25 Dreg', 'type': 'Water Electrical Conductivity 25 Dreg'}, 'er': {'unit': 'Ω.cm', 'chart': 'line', 'icon': 'fa-ruler-vertical', 'legend': 'Electrical Resistivity ', 'type': 'Water Electrical Resistivity '}, 'pp': {'unit': '%', 'chart': 'line', 'icon': 'mi_build', 'legend': 'Power Pump', 'type': 'Power Pump'}, 'mass': {'unit': 'Kg', 'chart': 'column', 'icon': 'fa-balance-scale', 'legend': 'Mass Kg', 'type': 'Mass'}, 'mc': {'unit': '%', 'chart': 'line', 'icon': 'fa-thermometer', 'legend': 'Moisture Content (dry basis)', 'type': 'Moisture Content (dry basis)'}, 'mass_mv': {'unit': 'mV', 'chart': 'line', 'icon': 'fa-thermometer', 'legend': 'Mass in mV', 'type': 'Mass_mv'}, 'no': {'unit': '&#181;g/m&#179;', 'chart': 'line', 'icon': 'NO', 'legend': 'Concentration (μg/m3)', 'type': 'Nitric Oxide'}, 'nomv': {'unit': 'mV', 'chart': 'line', 'icon': 'NO mV', 'legend': ' Concentration (mV)', 'type': 'Nitric Oxide - mV'}, 'c6h6': {'unit': '&#181;g/m&#179;', 'chart': 'line', 'icon': 'C&#8326;H&#8326;', 'legend': 'Concentration (μg/m3)', 'type': 'Benzene'}, 'c6h6mv': {'unit': 'mV', 'chart': 'line', 'icon': 'C&#8326;H&#8326; mV', 'legend': 'Concentration (mV)', 'type': 'Benzene - mV'}, 'vbat': {'unit': 'u', 'chart': 'line', 'icon': 'fa-battery-full', 'legend': 'Voltage (V)', 'type': 'Battery Voltage'}, 'db16k': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 16kHz'}, 'db12k5': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 12.5kHz'}, 'db10k': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 10kHz'}, 'db20k': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 20kHz'}, 'db8k': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 8kHz'}, 'db6k3': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 6.3kHz'}, 'db5k': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 5kHz'}, 'db4k': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 4kHz'}, 'db3k15': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 3.15kHz'}, 'db2k5': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 2.5kHz'}, 'db2k': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 2kHz'}, 'db1k6': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 1.6kHz'}, 'db1k25': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 1.25kHz'}, 'db1k': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 1kHz'}, 'db800': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 800Hz'}, 'db630': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 630Hz'}, 'db500': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 500Hz'}, 'db400': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 400Hz'}, 'db315': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 315Hz'}, 'db250': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 250Hz'}, 'db100': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 100Hz'}, 'db80': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 80Hz'}, 'db63': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 63Hz'}, 'db50': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 50Hz'}, 'db40': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 40Hz'}, 'db31h5': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 31.5Hz'}, 'db25': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 25Hz'}, 'db20': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 20Hz'}, 'db16': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 16Hz'}, 'db12h5': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 12.5Hz'}, 'db200': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 200Hz'}, 'db160': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 160Hz'}, 'db125': {'unit': 'dB(A)', 'chart': 'line', 'icon': 'fa-volume-up', 'legend': 'Noise Level (dB(A))', 'type': 'Noise Level 125Hz'}, 'rms1s1h80h': {'unit': 'mm/s', 'chart': 'column', 'icon': '1Hz-80Hz', 'legend': 'Vmax RMS 1s 1-80Hz (mm/s)', 'type': 'Vmax RMS 1s 1Hz-80Hz'}, 'rms1s16Hz250Hz': {'unit': 'mm/s', 'chart': 'column', 'icon': '16Hz-250Hz', 'legend': 'Vmax RMS 1s 16-250Hz (mm/s)', 'type': 'Vmax RMS 1s 16Hz-250Hz'}, 'VmaxPeak': {'unit': 'mm/s', 'chart': 'column', 'icon': 'MSp', 'legend': 'Vmax Pico (mm/s)', 'type': 'Vmax Pico'}, 'st1': {'unit': 'ºC', 'chart': 'line', 'icon': 'fa-thermometer', 'legend': 'soil temperature 1 (ºC)', 'type': 'Soil temperature 1'}, 'st2': {'unit': 'ºC', 'chart': 'line', 'icon': 'fa-thermometer', 'legend': 'Soil temperature 2 (ºC)', 'type': 'Soil temperature 2'}, 'st1mv': {'unit': 'mV', 'chart': 'line', 'icon': 'fa-thermometer', 'legend': 'Soil temperature 1 (mV)', 'type': 'Soil temperature 1 - mV'}, 'st2mv': {'unit': 'mV', 'chart': 'line', 'icon': 'fa-thermometer', 'legend': 'Soil temperature 2 (mV)', 'type': 'Soil temperature 2 - mV'}, 'sec1': {'unit': 'µS/cm', 'chart': 'line', 'icon': 'fa-bolt', 'legend': 'Soil Electrical Conductivity 1 (μS/cm)', 'type': 'Soil Electrical Conductivity 1'}, 'sec2': {'unit': 'µS/cm', 'chart': 'line', 'icon': 'fa-bolt', 'legend': 'Soil Electrical Conductivity 2 (μS/cm)', 'type': 'Soil Electrical Conductivity 2'}, 'sec1mv': {'unit': 'mV', 'chart': 'line', 'icon': 'EC mV', 'legend': 'Soil Electrical Conductivity 1 (mV)', 'type': 'Soil Electrical Conductivity 1 - mV'}, 'sec2mv': {'unit': 'mV', 'chart': 'line', 'icon': 'EC mV', 'legend': 'Soil Electrical Conductivity 2 (mV)', 'type': 'Soil Electrical Conductivity 2 - mV'}, 'vwc1': {'unit': '%', 'chart': 'line', 'icon': 'SM1', 'legend': 'Volumetric water content 1 (%)', 'type': 'Volumetric Water Content 1'}, 'vwc2': {'unit': '%', 'chart': 'line', 'icon': 'SM2', 'legend': 'Volumetric water content 2 (%)', 'type': 'Volumetric Water Content 2'}, 'vwc1mv': {'unit': 'mV', 'chart': 'line', 'icon': 'SM1 mV', 'legend': 'Volumetric Water Content 1 (mV)', 'type': 'Volumetric Water Content 1 - mV'}, 'vwc2mv': {'unit': 'mV', 'chart': 'line', 'icon': 'SM2 mV', 'legend': 'Volumetric Water Content 2 (mV)', 'type': 'Volumetric Water Content 2 - mV'}, 'mass_ax_mv': {'unit': 'mV', 'chart': 'line', 'icon': 'mi_build', 'legend': 'Mass in mV', 'type': 'Mass_ax_mv'}, 'vmax': {'unit': 'mm/s', 'chart': 'column', 'icon': 'Vmax', 'legend': 'Vmax (mm/s)', 'type': 'Vmax'}}

}
