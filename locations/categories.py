from enum import Enum

class Code(Enum):
    RESTAURANT = "100-1000-0000"
    CASUAL_DINING = "100-1000-0001"
    FINE_DINING = "100-1000-0002"
    TAKE_OUT_AND_DELIVERY_ONLY = "100-1000-0003"
    FOOD_MARKET_STALL = "100-1000-0004"
    TAQUERIA = "100-1000-0005"
    DELI = "100-1000-0006"
    CAFETERIA = "100-1000-0007"
    BISTRO = "100-1000-0008"
    FAST_FOOD = "100-1000-0009"
    COFFEE_TEA = "100-1100-0000"
    COFFEE_SHOP = "100-1100-0010"
    TEA_HOUSE = "100-1100-0331"
    NIGHTLIFE_ENTERTAINMENT = "200-2000-0000"
    BAR_OR_PUB = "200-2000-0011"
    NIGHT_CLUB = "200-2000-0012"
    DANCING = "200-2000-0013"
    KARAOKE = "200-2000-0014"
    LIVE_ENTERTAINMENT_MUSIC = "200-2000-0015"
    BILLIARDS_POOL_HALL = "200-2000-0016"
    VIDEO_ARCADE_GAME_ROOM = "200-2000-0017"
    JAZZ_CLUB = "200-2000-0018"
    BEER_GARDEN = "200-2000-0019"
    ADULT_ENTERTAINMENT = "200-2000-0306"
    COCKTAIL_LOUNGE = "200-2000-0368"
    CINEMA = "200-2100-0019"
    THEATRE_MUSIC_AND_CULTURE = "200-2200-0000"
    PERFORMING_ARTS = "200-2200-0020"
    GAMBLING_LOTTERY_BETTING = "200-2300-0000"
    CASINO = "200-2300-0021"
    LOTTERY_BOOTH = "200-2300-0022"
    LANDMARK_ATTRACTION = "300-3000-0000"
    TOURIST_ATTRACTION = "300-3000-0023"
    GALLERY = "300-3000-0024"
    HISTORICAL_MONUMENT = "300-3000-0025"
    CASTLE = "300-3000-0030"
    WINERY = "300-3000-0065"
    NAMED_INTERSECTION_CHOWK = "300-3000-0232"
    BREWERY = "300-3000-0350"
    DISTILLERY = "300-3000-0351"
    MUSEUM = "300-3100-0000"
    SCIENCE_MUSEUM = "300-3100-0026"
    CHILDRENS_MUSEUM = "300-3100-0027"
    HISTORY_MUSEUM = "300-3100-0028"
    ART_MUSEUM = "300-3100-0029"
    RELIGIOUS_PLACE = "300-3200-0000"
    CHURCH = "300-3200-0030"
    TEMPLE = "300-3200-0031"
    SYNAGOGUE = "300-3200-0032"
    ASHRAM = "300-3200-0033"
    MOSQUE = "300-3200-0034"
    OTHER_PLACE_OF_WORSHIP = "300-3200-0309"
    GURDWARA = "300-3200-0375"
    PAGODA = "300-3200-0376"
    BODY_OF_WATER = "350-3500-0233"
    RESERVOIR = "350-3500-0234"
    WATERFALL = "350-3500-0235"
    BAY_HARBOR = "350-3500-0300"
    RIVER = "350-3500-0302"
    CANAL = "350-3500-0303"
    LAKE = "350-3500-0304"
    MOUNTAIN_OR_HILL = "350-3510-0236"
    MOUNTAIN_PASSES = "350-3510-0237"
    MOUNTAIN_PEAKS = "350-3510-0238"
    UNDERSEA_FEATURE = "350-3520-0224"
    FOREST_HEATH_OR_OTHER_VEGETATION = "350-3522-0239"
    NATURAL_AND_GEOGRAPHICAL = "350-3550-0336"
    PUBLIC_SPORTS_AIRPORT = "400-4000-4580"
    AIRPORT = "400-4000-4581"
    AIRPORT_TERMINAL = "400-4000-4582"
    TRAIN_STATION = "400-4100-0035"
    BUS_STATION = "400-4100-0036"
    UNDERGROUND_TRAIN_SUBWAY = "400-4100-0037"
    COMMUTER_RAIL_STATION = "400-4100-0038"
    COMMUTER_TRAIN = "400-4100-0039"
    PUBLIC_TRANSIT_ACCESS = "400-4100-0040"
    TRANSPORTATION_SERVICE = "400-4100-0041"
    BUS_STOP = "400-4100-0042"
    LOCAL_TRANSIT = "400-4100-0043"
    FERRY_TERMINAL = "400-4100-0044"
    BOAT_FERRY = "400-4100-0045"
    RAIL_FERRY = "400-4100-0046"
    TAXI_STAND = "400-4100-0047"
    HIGHWAY_EXIT = "400-4100-0226"
    TOLLBOOTH = "400-4100-0326"
    LIGHTRAIL = "400-4100-0337"
    WATER_TRANSIT = "400-4100-0338"
    MONORAIL = "400-4100-0339"
    AERIAL_TRAMWAY = "400-4100-0340"
    BUS_RAPID_TRANSIT = "400-4100-0341"
    INCLINED_RAIL = "400-4100-0342"
    BICYCLE_SHARING_LOCATION = "400-4100-0347"
    BICYCLE_PARKING = "400-4100-0348"
    WEIGH_STATION = "400-4200-0048"
    CARGO_CENTER = "400-4200-0049"
    RAIL_YARD = "400-4200-0050"
    SEAPORT_HARBOUR = "400-4200-0051"
    AIRPORT_CARGO = "400-4200-0052"
    COURIERS = "400-4200-0240"
    CARGO_TRANSPORTATION = "400-4200-0241"
    DELIVERY_ENTRANCE = "400-4200-0311"
    LOADING_DOCK = "400-4200-0312"
    LOADING_ZONE = "400-4200-0313"
    REST_AREA = "400-4300-0000"
    COMPLETE_REST_AREA = "400-4300-0199"
    PARKING_AND_RESTROOM_ONLY_REST_AREA = "400-4300-0200"
    PARKING_ONLY_REST_AREA = "400-4300-0201"
    MOTORWAY_SERVICE_REST_AREA = "400-4300-0202"
    SCENIC_OVERLOOK_REST_AREA = "400-4300-0308"
    HOTEL_OR_MOTEL = "500-5000-0000"
    HOTEL = "500-5000-0053"
    MOTEL = "500-5000-0054"
    LODGING = "500-5100-0000"
    HOSTEL = "500-5100-0055"
    CAMPGROUND = "500-5100-0056"
    GUEST_HOUSE = "500-5100-0057"
    BED_AND_BREAKFAST = "500-5100-0058"
    HOLIDAY_PARK = "500-5100-0059"
    SHORT_TIME_MOTEL = "500-5100-0060"
    RYOKAN = "500-5100-0061"
    OUTDOOR_RECREATION = "550-5510-0000"
    PARK_RECREATION_AREA = "550-5510-0202"
    SPORTS_FIELD = "550-5510-0203"
    GARDEN = "550-5510-0204"
    BEACH = "550-5510-0205"
    RECREATION_CENTER = "550-5510-0206"
    SKI_LIFT = "550-5510-0227"
    SCENIC_POINT = "550-5510-0242"
    OFF_ROAD_TRAILHEAD = "550-5510-0358"
    TRAILHEAD = "550-5510-0359"
    OFF_ROAD_VEHICLE_AREA = "550-5510-0374"
    CAMPSITE = "550-5510-0378"
    OUTDOOR_SERVICE = "550-5510-0379"
    RANGER_STATION = "550-5510-0380"
    BICYCLE_SERVICE = "550-5510-0387"
    LEISURE = "550-5520-0000"
    AMUSEMENT_PARK = "550-5520-0207"
    ZOO = "550-5520-0208"
    WILD_ANIMAL_PARK = "550-5520-0209"
    WILDLIFE_REFUGE = "550-5520-0210"
    AQUARIUM = "550-5520-0211"
    SKI_RESORT = "550-5520-0212"
    ANIMAL_PARK = "550-5520-0228"
    WATER_PARK = "550-5520-0357"
    CONVENIENCE_STORE = "600-6000-0061"
    SHOPPING_MALL = "600-6100-0062"
    DEPARTMENT_STORE = "600-6200-0063"
    FOOD_BEVERAGE_SPECIALTY_STORE = "600-6300-0064"
    GROCERY = "600-6300-0066"
    SPECIALTY_FOOD_STORE = "600-6300-0067"
    WINE_AND_LIQUOR = "600-6300-0068"
    BAKERY_AND_BAKED_GOODS_STORE = "600-6300-0244"
    SWEET_SHOP = "600-6300-0245"
    DOUGHNUT_SHOP = "600-6300-0246"
    BUTCHER = "600-6300-0363"
    DAIRY_GOODS = "600-6300-0364"
    DRUGSTORE_OR_PHARMACY = "600-6400-0000"
    DRUGSTORE = "600-6400-0069"
    PHARMACY = "600-6400-0070"
    CONSUMER_ELECTRONICS_STORE = "600-6500-0072"
    MOBILE_RETAILER = "600-6500-0073"
    MOBILE_SERVICE_CENTER = "600-6500-0074"
    COMPUTER_AND_SOFTWARE = "600-6500-0075"
    ENTERTAINMENT_ELECTRONICS = "600-6500-0076"
    HARDWARE_HOUSE_AND_GARDEN = "600-6600-0000"
    HOME_IMPROVEMENT = "600-6600-0077"
    HOME_SPECIALTY_STORE = "600-6600-0078"
    FLOOR_AND_CARPET = "600-6600-0079"
    FURNITURE_STORE = "600-6600-0080"
    GARDEN_CENTER = "600-6600-0082"
    GLASS_AND_WINDOW = "600-6600-0083"
    LUMBER = "600-6600-0084"
    MAJOR_APPLIANCE = "600-6600-0085"
    POWER_EQUIPMENT_DEALER = "600-6600-0310"
    PAINT_STORE = "600-6600-0319"
    OTHER_BOOKSHOP = "600-6700-0000"
    BOOKSTORE = "600-6700-0087"
    CLOTHING_AND_ACCESSORIES = "600-6800-0000"
    MENS_APPAREL = "600-6800-0089"
    WOMENS_APPAREL = "600-6800-0090"
    CHILDRENS_APPAREL = "600-6800-0091"
    SHOES_FOOTWEAR = "600-6800-0092"
    SPECIALTY_CLOTHING_STORE = "600-6800-0093"
    CONSUMER_GOODS = "600-6900-0000"
    SPORTING_GOODS_STORE = "600-6900-0094"
    OFFICE_SUPPLY_AND_SERVICES_STORE = "600-6900-0095"
    SPECIALTY_STORE = "600-6900-0096"
    PET_SUPPLY = "600-6900-0097"
    WAREHOUSE_WHOLESALE_STORE = "600-6900-0098"
    GENERAL_MERCHANDISE = "600-6900-0099"
    DISCOUNT_STORE = "600-6900-0100"
    FLOWERS_AND_JEWELRY = "600-6900-0101"
    VARIETY_STORE = "600-6900-0102"
    GIFT_ANTIQUE_AND_ART = "600-6900-0103"
    RECORD_CD_AND_VIDEO = "600-6900-0105"
    VIDEO_AND_GAME_RENTAL = "600-6900-0106"
    CIGAR_AND_TOBACCO_SHOP = "600-6900-0107"
    VAPING_STORE = "600-6900-0108"
    BICYCLE_AND_BICYCLE_ACCESSORIES_SHOP = "600-6900-0246"
    MARKET = "600-6900-0247"
    MOTORCYCLE_ACCESSORIES = "600-6900-0248"
    NON_STORE_RETAILERS = "600-6900-0249"
    PAWNSHOP = "600-6900-0250"
    USED_SECOND_HAND_MERCHANDISE_STORES = "600-6900-0251"
    ADULT_SHOP = "600-6900-0305"
    ARTS_AND_CRAFTS_SUPPLIES = "600-6900-0307"
    FLORIST = "600-6900-0355"
    JEWELER = "600-6900-0356"
    TOY_STORE = "600-6900-0358"
    HUNTING_FISHING_SHOP = "600-6900-0388"
    RUNNING_WALKING_SHOP = "600-6900-0389"
    SKATE_SHOP = "600-6900-0390"
    SKI_SHOP = "600-6900-0391"
    SNOWBOARD_SHOP = "600-6900-0392"
    SURF_SHOP = "600-6900-0393"
    BMX_SHOP = "600-6900-0394"
    CAMPING_HIKING_SHOP = "600-6900-0395"
    CANOE_KAYAK_SHOP = "600-6900-0396"
    CROSS_COUNTRY_SKI_SHOP = "600-6900-0397"
    TACK_SHOP = "600-6900-0398"
    HAIR_AND_BEAUTY = "600-6950-0000"
    BARBER = "600-6950-0399"
    NAIL_SALON = "600-6950-0400"
    HAIR_SALON = "600-6950-0401"
    BANK = "700-7000-0107"
    ATM = "700-7010-0108"
    MONEY_TRANSFERRING_SERVICE = "700-7050-0109"
    CHECK_CASHING_SERVICE_CURRENCY_EXCHANGE = "700-7050-0110"
    COMMUNICATION_MEDIA = "700-7100-0000"
    TELEPHONE_SERVICE = "700-7100-0134"
    COMMERCIAL_SERVICES = "700-7200-0000"
    ADVERTISING_MARKETING_PR_AND_MARKET_RESEARCH = "700-7200-0252"
    CATERING_AND_OTHER_FOOD_SERVICES = "700-7200-0253"
    CONSTRUCTION = "700-7200-0254"
    CUSTOMER_CARE_SERVICE_CENTER = "700-7200-0255"
    ENGINEERING_AND_SCIENTIFIC_SERVICES = "700-7200-0256"
    FARMING = "700-7200-0257"
    FOOD_PRODUCTION = "700-7200-0258"
    HUMAN_RESOURCES_AND_RECRUITING_SERVICES = "700-7200-0259"
    INVESTIGATION_SERVICES = "700-7200-0260"
    IT_AND_OFFICE_EQUIPMENT_SERVICES = "700-7200-0261"
    LANDSCAPING_SERVICES = "700-7200-0262"
    LOCKSMITHS_AND_SECURITY_SYSTEMS_SERVICES = "700-7200-0263"
    MANAGEMENT_AND_CONSULTING_SERVICES = "700-7200-0264"
    MANUFACTURING = "700-7200-0265"
    MINING = "700-7200-0266"
    MODELING_AGENCIES = "700-7200-0267"
    MOTORCYCLE_SERVICE_AND_MAINTENANCE = "700-7200-0268"
    ORGANIZATIONS_AND_SOCIETIES = "700-7200-0269"
    ENTERTAINMENT_AND_RECREATION = "700-7200-0270"
    FINANCE_AND_INSURANCE = "700-7200-0271"
    HEALTHCARE_AND_HEALTHCARE_SUPPORT_SERVICES = "700-7200-0272"
    RENTAL_AND_LEASING = "700-7200-0274"
    REPAIR_AND_MAINTENANCE_SERVICES = "700-7200-0275"
    PRINTING_AND_PUBLISHING = "700-7200-0276"
    SPECIALTY_TRADE_CONTRACTORS = "700-7200-0277"
    TOWING_SERVICE = "700-7200-0278"
    TRANSLATION_AND_INTERPRETATION_SERVICES = "700-7200-0279"
    APARTMENT_RENTAL_FLAT_RENTAL = "700-7200-0324"
    B2B_SALES_AND_SERVICES = "700-7200-0328"
    B2B_RESTAURANT_SERVICES = "700-7200-0329"
    AVIATION = "700-7200-0330"
    INTERIOR_AND_EXTERIOR_DESIGN = "700-7200-0342"
    PROPERTY_MANAGEMENT = "700-7200-0344"
    FINANCIAL_INVESTMENT_FIRM = "700-7200-0345"
    BUSINESS_FACILITY = "700-7250-0136"
    POLICE_BOX = "700-7300-0110"
    POLICE_STATION = "700-7300-0111"
    POLICE_SERVICES_SECURITY = "700-7300-0112"
    FIRE_DEPARTMENT = "700-7300-0113"
    AMBULANCE_SERVICES = "700-7300-0280"
    CONSUMER_SERVICES = "700-7400-0000"
    TRAVEL_AGENT_TICKETING = "700-7400-0133"
    DRY_CLEANING_AND_LAUNDRY = "700-7400-0137"
    ATTORNEY = "700-7400-0138"
    BOATING = "700-7400-0140"
    BUSINESS_SERVICE = "700-7400-0141"
    FUNERAL_DIRECTOR = "700-7400-0142"
    MOVER = "700-7400-0143"
    PHOTOGRAPHY = "700-7400-0144"
    REAL_ESTATE_SERVICES = "700-7400-0145"
    REPAIR_SERVICE = "700-7400-0146"
    SOCIAL_SERVICE = "700-7400-0147"
    STORAGE = "700-7400-0148"
    TAILOR_AND_ALTERATION = "700-7400-0149"
    TAX_SERVICE = "700-7400-0150"
    UTILITIES = "700-7400-0151"
    WASTE_AND_SANITARY = "700-7400-0152"
    BICYCLE_SERVICE_AND_MAINTENANCE = "700-7400-0281"
    BILL_PAYMENT_SERVICE = "700-7400-0282"
    BODY_PIERCING_AND_TATTOOS = "700-7400-0283"
    WEDDING_SERVICES_AND_BRIDAL_STUDIO = "700-7400-0284"
    INTERNET_CAFE = "700-7400-0285"
    KINDERGARTEN_AND_CHILDCARE = "700-7400-0286"
    MAID_SERVICES = "700-7400-0287"
    MARRIAGE_AND_MATCH_MAKING_SERVICES = "700-7400-0288"
    PUBLIC_ADMINISTRATION = "700-7400-0289"
    WELLNESS_CENTER_AND_SERVICES = "700-7400-0292"
    PET_CARE = "700-7400-0293"
    LEGAL_SERVICES = "700-7400-0327"
    TANNING_SALON = "700-7400-0343"
    RECYCLING_CENTER = "700-7400-0352"
    ELECTRICAL = "700-7400-0365"
    PLUMBING = "700-7400-0366"
    POST_OFFICE = "700-7450-0114"
    TOURIST_INFORMATION = "700-7460-0115"
    FUELING_STATION = "700-7600-0000"
    PETROL_GASOLINE_STATION = "700-7600-0116"
    EV_CHARGING_STATION = "700-7600-0322"
    EV_BATTERY_SWAP_STATION = "700-7600-0325"
    HYDROGEN_FUEL_STATION = "700-7600-0444"
    AUTOMOBILE_DEALERSHIP_NEW_CARS = "700-7800-0118"
    AUTOMOBILE_DEALERSHIP_USED_CARS = "700-7800-0119"
    MOTORCYCLE_DEALERSHIP = "700-7800-0120"
    CAR_REPAIR_SERVICE = "700-7850-0000"
    CAR_WASH_DETAILING = "700-7850-0121"
    CAR_REPAIR = "700-7850-0122"
    AUTO_PARTS = "700-7850-0123"
    EMISSION_TESTING = "700-7850-0124"
    TIRE_REPAIR = "700-7850-0125"
    TRUCK_REPAIR = "700-7850-0126"
    VAN_REPAIR = "700-7850-0127"
    ROAD_ASSISTANCE = "700-7850-0128"
    AUTOMOBILE_CLUB = "700-7850-0129"
    RENTAL_CAR_AGENCY = "700-7851-0117"
    TRUCK_SEMI_DEALER_SERVICES = "700-7900-0000"
    TRUCK_DEALERSHIP = "700-7900-0130"
    TRUCK_PARKING = "700-7900-0131"
    TRUCK_STOP_PLAZA = "700-7900-0132"
    TRUCK_WASH = "700-7900-0323"
    HOSPITAL_OR_HEALTH_CARE_FACILITY = "800-8000-0000"
    DENTIST_DENTAL_OFFICE = "800-8000-0154"
    FAMILY_GENERAL_PRACTICE_PHYSICIANS = "800-8000-0155"
    PSYCHIATRIC_INSTITUTE = "800-8000-0156"
    NURSING_HOME = "800-8000-0157"
    MEDICAL_SERVICES_CLINICS = "800-8000-0158"
    HOSPITAL = "800-8000-0159"
    OPTICAL = "800-8000-0161"
    VETERINARIAN = "800-8000-0162"
    HOSPITAL_EMERGENCY_ROOM = "800-8000-0325"
    THERAPIST = "800-8000-0340"
    CHIROPRACTOR = "800-8000-0341"
    BLOOD_BANK = "800-8000-0367"
    COVID_19_TESTING_SITE = "800-8000-0400"
    GOVERNMENT_OR_COMMUNITY_FACILITY = "800-8100-0000"
    CITY_HALL = "800-8100-0163"
    EMBASSY = "800-8100-0164"
    MILITARY_BASE = "800-8100-0165"
    COUNTY_COUNCIL = "800-8100-0168"
    CIVIC_COMMUNITY_CENTER = "800-8100-0169"
    COURT_HOUSE = "800-8100-0170"
    GOVERNMENT_OFFICE = "800-8100-0171"
    BORDER_CROSSING = "800-8100-0172"
    EDUCATION_FACILITY = "800-8200-0000"
    HIGHER_EDUCATION = "800-8200-0173"
    SCHOOL = "800-8200-0174"
    TRAINING_AND_DEVELOPMENT = "800-8200-0295"
    COACHING_INSTITUTE = "800-8200-0360"
    FINE_ARTS = "800-8200-0361"
    LANGUAGE_STUDIES = "800-8200-0362"
    OTHER_LIBRARY = "800-8300-0000"
    LIBRARY = "800-8300-0175"
    EVENT_SPACES = "800-8400-0000"
    BANQUET_HALL = "800-8400-0139"
    CONVENTION_EXHIBITION_CENTER = "800-8400-0176"
    PARKING = "800-8500-0000"
    PARKING_GARAGE_PARKING_HOUSE = "800-8500-0177"
    PARKING_LOT = "800-8500-0178"
    PARK_AND_RIDE = "800-8500-0179"
    MOTORCYCLE_MOPED_AND_SCOOTER_PARKING = "800-8500-0200"
    CELLPHONE_PARKING_LOT = "800-8500-0315"
    SPORTS_FACILITY_VENUE = "800-8600-0000"
    SPORTS_COMPLEX_STADIUM = "800-8600-0180"
    ICE_SKATING_RINK = "800-8600-0181"
    SWIMMING_POOL = "800-8600-0182"
    TENNIS_COURT = "800-8600-0183"
    BOWLING_CENTER = "800-8600-0184"
    INDOOR_SKI = "800-8600-0185"
    HOCKEY = "800-8600-0186"
    RACQUETBALL_COURT = "800-8600-0187"
    SHOOTING_RANGE = "800-8600-0188"
    SOCCER_CLUB = "800-8600-0189"
    SQUASH_COURT = "800-8600-0190"
    FITNESS_HEALTH_CLUB = "800-8600-0191"
    INDOOR_SPORTS = "800-8600-0192"
    GOLF_COURSE = "800-8600-0193"
    GOLF_PRACTICE_RANGE = "800-8600-0194"
    RACE_TRACK = "800-8600-0195"
    SPORTING_INSTRUCTION_AND_CAMPS = "800-8600-0196"
    SPORTS_ACTIVITIES = "800-8600-0197"
    BASKETBALL = "800-8600-0199"
    BADMINTON = "800-8600-0200"
    RUGBY = "800-8600-0314"
    DIVING_CENTER = "800-8600-0316"
    BIKE_PARK = "800-8600-0376"
    BMX_TRACK = "800-8600-0377"
    RUNNING_TRACK = "800-8600-0381"
    FACILITIES = "800-8700-0000"
    CEMETERY = "800-8700-0166"
    CREMATORIUM = "800-8700-0167"
    PUBLIC_RESTROOM_TOILETS = "800-8700-0198"
    CLUBHOUSE = "800-8700-0296"
    REGISTRATION_OFFICE = "800-8700-0298"
    OUTDOOR_AREA_COMPLEX = "900-9200-0000"
    INDUSTRIAL_ZONE = "900-9200-0218"
    MARINA = "900-9200-0219"
    RV_PARKS = "900-9200-0220"
    COLLECTIVE_COMMUNITY = "900-9200-0299"
    ISLAND = "900-9200-0301"
    MEETING_POINT = "900-9200-0386"
    BUILDING = "900-9300-0000"
    RESIDENTIAL_AREA_BUILDING = "900-9300-0221"


class Name(Enum):
    RESTAURANT = "Restaurant"
    CASUAL_DINING = "Casual Dining"
    FINE_DINING = "Fine Dining"
    TAKE_OUT_AND_DELIVERY_ONLY = "Take Out and Delivery Only"
    FOOD_MARKET_STALL = "Food Market-Stall"
    TAQUERIA = "Taqueria"
    DELI = "Deli"
    CAFETERIA = "Cafeteria"
    BISTRO = "Bistro"
    FAST_FOOD = "Fast Food"
    COFFEE_TEA = "Coffee-Tea"
    COFFEE_SHOP = "Coffee Shop"
    TEA_HOUSE = "Tea House"
    NIGHTLIFE_ENTERTAINMENT = "Nightlife-Entertainment"
    BAR_OR_PUB = "Bar or Pub"
    NIGHT_CLUB = "Night Club"
    DANCING = "Dancing"
    KARAOKE = "Karaoke"
    LIVE_ENTERTAINMENT_MUSIC = "Live Entertainment-Music"
    BILLIARDS_POOL_HALL = "Billiards-Pool Hall"
    VIDEO_ARCADE_GAME_ROOM = "Video Arcade-Game Room"
    JAZZ_CLUB = "Jazz Club"
    BEER_GARDEN = "Beer Garden"
    ADULT_ENTERTAINMENT = "Adult Entertainment"
    COCKTAIL_LOUNGE = "Cocktail Lounge"
    CINEMA = "Cinema"
    THEATRE_MUSIC_AND_CULTURE = "Theatre, Music and Culture"
    PERFORMING_ARTS = "Performing Arts"
    GAMBLING_LOTTERY_BETTING = "Gambling-Lottery-Betting"
    CASINO = "Casino"
    LOTTERY_BOOTH = "Lottery Booth"
    LANDMARK_ATTRACTION = "Landmark-Attraction"
    TOURIST_ATTRACTION = "Tourist Attraction"
    GALLERY = "Gallery"
    HISTORICAL_MONUMENT = "Historical Monument"
    CASTLE = "Castle"
    WINERY = "Winery"
    NAMED_INTERSECTION_CHOWK = "Named Intersection-Chowk"
    BREWERY = "Brewery"
    DISTILLERY = "Distillery"
    MUSEUM = "Museum"
    SCIENCE_MUSEUM = "Science Museum"
    CHILDRENS_MUSEUM = "Children's Museum"
    HISTORY_MUSEUM = "History Museum"
    ART_MUSEUM = "Art Museum"
    RELIGIOUS_PLACE = "Religious Place"
    CHURCH = "Church"
    TEMPLE = "Temple"
    SYNAGOGUE = "Synagogue"
    ASHRAM = "Ashram"
    MOSQUE = "Mosque"
    OTHER_PLACE_OF_WORSHIP = "Other Place of Worship"
    GURDWARA = "Gurdwara"
    PAGODA = "Pagoda"
    BODY_OF_WATER = "Body of Water"
    RESERVOIR = "Reservoir"
    WATERFALL = "Waterfall"
    BAY_HARBOR = "Bay-Harbor"
    RIVER = "River"
    CANAL = "Canal"
    LAKE = "Lake"
    MOUNTAIN_OR_HILL = "Mountain or Hill"
    MOUNTAIN_PASSES = "Mountain Passes"
    MOUNTAIN_PEAKS = "Mountain Peaks"
    UNDERSEA_FEATURE = "Undersea Feature"
    FOREST_HEATH_OR_OTHER_VEGETATION = "Forest, Heath or Other Vegetation"
    NATURAL_AND_GEOGRAPHICAL = "Natural and Geographical"
    PUBLIC_SPORTS_AIRPORT = "Public Sports Airport"
    AIRPORT = "Airport"
    AIRPORT_TERMINAL = "Airport Terminal"
    TRAIN_STATION = "Train Station"
    BUS_STATION = "Bus Station"
    UNDERGROUND_TRAIN_SUBWAY = "Underground Train-Subway"
    COMMUTER_RAIL_STATION = "Commuter Rail Station"
    COMMUTER_TRAIN = "Commuter Train"
    PUBLIC_TRANSIT_ACCESS = "Public Transit Access"
    TRANSPORTATION_SERVICE = "Transportation Service"
    BUS_STOP = "Bus Stop"
    LOCAL_TRANSIT = "Local Transit"
    FERRY_TERMINAL = "Ferry Terminal"
    BOAT_FERRY = "Boat Ferry"
    RAIL_FERRY = "Rail Ferry"
    TAXI_STAND = "Taxi Stand"
    HIGHWAY_EXIT = "Highway Exit"
    TOLLBOOTH = "Tollbooth"
    LIGHTRAIL = "Lightrail"
    WATER_TRANSIT = "Water Transit"
    MONORAIL = "Monorail"
    AERIAL_TRAMWAY = "Aerial Tramway"
    BUS_RAPID_TRANSIT = "Bus Rapid Transit"
    INCLINED_RAIL = "Inclined Rail"
    BICYCLE_SHARING_LOCATION = "Bicycle Sharing Location"
    BICYCLE_PARKING = "Bicycle Parking"
    WEIGH_STATION = "Weigh Station"
    CARGO_CENTER = "Cargo Center"
    RAIL_YARD = "Rail Yard"
    SEAPORT_HARBOUR = "Seaport-Harbour"
    AIRPORT_CARGO = "Airport Cargo"
    COURIERS = "Couriers"
    CARGO_TRANSPORTATION = "Cargo Transportation"
    DELIVERY_ENTRANCE = "Delivery Entrance"
    LOADING_DOCK = "Loading Dock"
    LOADING_ZONE = "Loading Zone"
    REST_AREA = "Rest Area"
    COMPLETE_REST_AREA = "Complete Rest Area"
    PARKING_AND_RESTROOM_ONLY_REST_AREA = "Parking and Restroom Only Rest Area"
    PARKING_ONLY_REST_AREA = "Parking Only Rest Area"
    MOTORWAY_SERVICE_REST_AREA = "Motorway Service Rest Area"
    SCENIC_OVERLOOK_REST_AREA = "Scenic Overlook Rest Area"
    HOTEL_OR_MOTEL = "Hotel or Motel"
    HOTEL = "Hotel"
    MOTEL = "Motel"
    LODGING = "Lodging"
    HOSTEL = "Hostel"
    CAMPGROUND = "Campground"
    GUEST_HOUSE = "Guest House"
    BED_AND_BREAKFAST = "Bed and Breakfast"
    HOLIDAY_PARK = "Holiday Park"
    SHORT_TIME_MOTEL = "Short-Time Motel"
    RYOKAN = "Ryokan"
    OUTDOOR_RECREATION = "Outdoor-Recreation"
    PARK_RECREATION_AREA = "Park-Recreation Area"
    SPORTS_FIELD = "Sports Field"
    GARDEN = "Garden"
    BEACH = "Beach"
    RECREATION_CENTER = "Recreation Center"
    SKI_LIFT = "Ski Lift"
    SCENIC_POINT = "Scenic Point"
    OFF_ROAD_TRAILHEAD = "Off Road Trailhead"
    TRAILHEAD = "Trailhead"
    OFF_ROAD_VEHICLE_AREA = "Off-Road Vehicle Area"
    CAMPSITE = "Campsite"
    OUTDOOR_SERVICE = "Outdoor Service"
    RANGER_STATION = "Ranger Station"
    BICYCLE_SERVICE = "Bicycle Service"
    LEISURE = "Leisure"
    AMUSEMENT_PARK = "Amusement Park"
    ZOO = "Zoo"
    WILD_ANIMAL_PARK = "Wild Animal Park"
    WILDLIFE_REFUGE = "Wildlife Refuge"
    AQUARIUM = "Aquarium"
    SKI_RESORT = "Ski Resort"
    ANIMAL_PARK = "Animal Park"
    WATER_PARK = "Water Park"
    CONVENIENCE_STORE = "Convenience Store"
    SHOPPING_MALL = "Shopping Mall"
    DEPARTMENT_STORE = "Department Store"
    FOOD_BEVERAGE_SPECIALTY_STORE = "Food-Beverage Specialty Store"
    GROCERY = "Grocery"
    SPECIALTY_FOOD_STORE = "Specialty Food Store"
    WINE_AND_LIQUOR = "Wine and Liquor"
    BAKERY_AND_BAKED_GOODS_STORE = "Bakery and Baked Goods Store"
    SWEET_SHOP = "Sweet Shop"
    DOUGHNUT_SHOP = "Doughnut Shop"
    BUTCHER = "Butcher"
    DAIRY_GOODS = "Dairy Goods"
    DRUGSTORE_OR_PHARMACY = "Drugstore or Pharmacy"
    DRUGSTORE = "Drugstore"
    PHARMACY = "Pharmacy"
    CONSUMER_ELECTRONICS_STORE = "Consumer Electronics Store"
    MOBILE_RETAILER = "Mobile Retailer"
    MOBILE_SERVICE_CENTER = "Mobile Service Center"
    COMPUTER_AND_SOFTWARE = "Computer and Software"
    ENTERTAINMENT_ELECTRONICS = "Entertainment Electronics"
    HARDWARE_HOUSE_AND_GARDEN = "Hardware, House and Garden"
    HOME_IMPROVEMENT = "Home Improvement"
    HOME_SPECIALTY_STORE = "Home Specialty Store"
    FLOOR_AND_CARPET = "Floor and Carpet"
    FURNITURE_STORE = "Furniture Store"
    GARDEN_CENTER = "Garden Center"
    GLASS_AND_WINDOW = "Glass and Window"
    LUMBER = "Lumber"
    MAJOR_APPLIANCE = "Major Appliance"
    POWER_EQUIPMENT_DEALER = "Power Equipment Dealer"
    PAINT_STORE = "Paint Store"
    OTHER_BOOKSHOP = "Other Bookshop"
    BOOKSTORE = "Bookstore"
    CLOTHING_AND_ACCESSORIES = "Clothing and Accessories"
    MENS_APPAREL = "Men's Apparel"
    WOMENS_APPAREL = "Women's Apparel"
    CHILDRENS_APPAREL = "Children's Apparel"
    SHOES_FOOTWEAR = "Shoes-Footwear"
    SPECIALTY_CLOTHING_STORE = "Specialty Clothing Store"
    CONSUMER_GOODS = "Consumer Goods"
    SPORTING_GOODS_STORE = "Sporting Goods Store"
    OFFICE_SUPPLY_AND_SERVICES_STORE = "Office Supply and Services Store"
    SPECIALTY_STORE = "Specialty Store"
    PET_SUPPLY = "Pet Supply"
    WAREHOUSE_WHOLESALE_STORE = "Warehouse-Wholesale Store"
    GENERAL_MERCHANDISE = "General Merchandise"
    DISCOUNT_STORE = "Discount Store"
    FLOWERS_AND_JEWELRY = "Flowers and Jewelry"
    VARIETY_STORE = "Variety Store"
    GIFT_ANTIQUE_AND_ART = "Gift, Antique and Art"
    RECORD_CD_AND_VIDEO = "Record, CD and Video"
    VIDEO_AND_GAME_RENTAL = "Video and Game Rental"
    CIGAR_AND_TOBACCO_SHOP = "Cigar and Tobacco Shop"
    VAPING_STORE = "Vaping Store"
    BICYCLE_AND_BICYCLE_ACCESSORIES_SHOP = "Bicycle and Bicycle Accessories Shop"
    MARKET = "Market"
    MOTORCYCLE_ACCESSORIES = "Motorcycle Accessories"
    NON_STORE_RETAILERS = "Non-Store Retailers"
    PAWNSHOP = "Pawnshop"
    USED_SECOND_HAND_MERCHANDISE_STORES = "Used-Second Hand Merchandise Stores"
    ADULT_SHOP = "Adult Shop"
    ARTS_AND_CRAFTS_SUPPLIES = "Arts and Crafts Supplies"
    FLORIST = "Florist"
    JEWELER = "Jeweler"
    TOY_STORE = "Toy Store"
    HUNTING_FISHING_SHOP = "Hunting-Fishing Shop"
    RUNNING_WALKING_SHOP = "Running-Walking Shop"
    SKATE_SHOP = "Skate Shop"
    SKI_SHOP = "Ski Shop"
    SNOWBOARD_SHOP = "Snowboard Shop"
    SURF_SHOP = "Surf Shop"
    BMX_SHOP = "BMX Shop"
    CAMPING_HIKING_SHOP = "Camping-Hiking Shop"
    CANOE_KAYAK_SHOP = "Canoe-Kayak Shop"
    CROSS_COUNTRY_SKI_SHOP = "Cross Country Ski Shop"
    TACK_SHOP = "Tack Shop"
    HAIR_AND_BEAUTY = "Hair and Beauty"
    BARBER = "Barber"
    NAIL_SALON = "Nail Salon"
    HAIR_SALON = "Hair Salon"
    BANK = "Bank"
    ATM = "ATM"
    MONEY_TRANSFERRING_SERVICE = "Money Transferring Service"
    CHECK_CASHING_SERVICE_CURRENCY_EXCHANGE = "Check Cashing Service-Currency Exchange"
    COMMUNICATION_MEDIA = "Communication-Media"
    TELEPHONE_SERVICE = "Telephone Service"
    COMMERCIAL_SERVICES = "Commercial Services"
    ADVERTISING_MARKETING_PR_AND_MARKET_RESEARCH = "Advertising-Marketing, PR and Market Research"
    CATERING_AND_OTHER_FOOD_SERVICES = "Catering and Other Food Services"
    CONSTRUCTION = "Construction"
    CUSTOMER_CARE_SERVICE_CENTER = "Customer Care-Service Center"
    ENGINEERING_AND_SCIENTIFIC_SERVICES = "Engineering and Scientific Services"
    FARMING = "Farming"
    FOOD_PRODUCTION = "Food Production"
    HUMAN_RESOURCES_AND_RECRUITING_SERVICES = "Human Resources and Recruiting Services"
    INVESTIGATION_SERVICES = "Investigation Services"
    IT_AND_OFFICE_EQUIPMENT_SERVICES = "IT and Office Equipment Services"
    LANDSCAPING_SERVICES = "Landscaping Services"
    LOCKSMITHS_AND_SECURITY_SYSTEMS_SERVICES = "Locksmiths and Security Systems Services"
    MANAGEMENT_AND_CONSULTING_SERVICES = "Management and Consulting Services"
    MANUFACTURING = "Manufacturing"
    MINING = "Mining"
    MODELING_AGENCIES = "Modeling Agencies"
    MOTORCYCLE_SERVICE_AND_MAINTENANCE = "Motorcycle Service and Maintenance"
    ORGANIZATIONS_AND_SOCIETIES = "Organizations and Societies"
    ENTERTAINMENT_AND_RECREATION = "Entertainment and Recreation"
    FINANCE_AND_INSURANCE = "Finance and Insurance"
    HEALTHCARE_AND_HEALTHCARE_SUPPORT_SERVICES = "Healthcare and Healthcare Support Services"
    RENTAL_AND_LEASING = "Rental and Leasing"
    REPAIR_AND_MAINTENANCE_SERVICES = "Repair and Maintenance Services"
    PRINTING_AND_PUBLISHING = "Printing and Publishing"
    SPECIALTY_TRADE_CONTRACTORS = "Specialty Trade Contractors"
    TOWING_SERVICE = "Towing Service"
    TRANSLATION_AND_INTERPRETATION_SERVICES = "Translation and Interpretation Services"
    APARTMENT_RENTAL_FLAT_RENTAL = "Apartment Rental-Flat Rental"
    B2B_SALES_AND_SERVICES = "B2B Sales and Services"
    B2B_RESTAURANT_SERVICES = "B2B Restaurant Services"
    AVIATION = "Aviation"
    INTERIOR_AND_EXTERIOR_DESIGN = "Interior and Exterior Design"
    PROPERTY_MANAGEMENT = "Property Management"
    FINANCIAL_INVESTMENT_FIRM = "Financial Investment Firm"
    BUSINESS_FACILITY = "Business Facility"
    POLICE_BOX = "Police Box"
    POLICE_STATION = "Police Station"
    POLICE_SERVICES_SECURITY = "Police Services-Security"
    FIRE_DEPARTMENT = "Fire Department"
    AMBULANCE_SERVICES = "Ambulance Services"
    CONSUMER_SERVICES = "Consumer Services"
    TRAVEL_AGENT_TICKETING = "Travel Agent-Ticketing"
    DRY_CLEANING_AND_LAUNDRY = "Dry Cleaning and Laundry"
    ATTORNEY = "Attorney"
    BOATING = "Boating"
    BUSINESS_SERVICE = "Business Service"
    FUNERAL_DIRECTOR = "Funeral Director"
    MOVER = "Mover"
    PHOTOGRAPHY = "Photography"
    REAL_ESTATE_SERVICES = "Real Estate Services"
    REPAIR_SERVICE = "Repair Service"
    SOCIAL_SERVICE = "Social Service"
    STORAGE = "Storage"
    TAILOR_AND_ALTERATION = "Tailor and Alteration"
    TAX_SERVICE = "Tax Service"
    UTILITIES = "Utilities"
    WASTE_AND_SANITARY = "Waste and Sanitary"
    BICYCLE_SERVICE_AND_MAINTENANCE = "Bicycle Service and Maintenance"
    BILL_PAYMENT_SERVICE = "Bill Payment Service"
    BODY_PIERCING_AND_TATTOOS = "Body Piercing and Tattoos"
    WEDDING_SERVICES_AND_BRIDAL_STUDIO = "Wedding Services and Bridal Studio"
    INTERNET_CAFE = "Internet Cafe"
    KINDERGARTEN_AND_CHILDCARE = "Kindergarten and Childcare"
    MAID_SERVICES = "Maid Services"
    MARRIAGE_AND_MATCH_MAKING_SERVICES = "Marriage and Match Making Services"
    PUBLIC_ADMINISTRATION = "Public Administration"
    WELLNESS_CENTER_AND_SERVICES = "Wellness Center and Services"
    PET_CARE = "Pet Care"
    LEGAL_SERVICES = "Legal Services"
    TANNING_SALON = "Tanning Salon"
    RECYCLING_CENTER = "Recycling Center"
    ELECTRICAL = "Electrical"
    PLUMBING = "Plumbing"
    POST_OFFICE = "Post Office"
    TOURIST_INFORMATION = "Tourist Information"
    FUELING_STATION = "Fueling Station"
    PETROL_GASOLINE_STATION = "Petrol-Gasoline Station"
    EV_CHARGING_STATION = "EV Charging Station"
    EV_BATTERY_SWAP_STATION = "EV Battery Swap Station"
    HYDROGEN_FUEL_STATION = "Hydrogen Fuel Station"
    AUTOMOBILE_DEALERSHIP_NEW_CARS = "Automobile Dealership-New Cars"
    AUTOMOBILE_DEALERSHIP_USED_CARS = "Automobile Dealership-Used Cars"
    MOTORCYCLE_DEALERSHIP = "Motorcycle Dealership"
    CAR_REPAIR_SERVICE = "Car Repair-Service"
    CAR_WASH_DETAILING = "Car Wash-Detailing"
    CAR_REPAIR = "Car Repair"
    AUTO_PARTS = "Auto Parts"
    EMISSION_TESTING = "Emission Testing"
    TIRE_REPAIR = "Tire Repair"
    TRUCK_REPAIR = "Truck Repair"
    VAN_REPAIR = "Van Repair"
    ROAD_ASSISTANCE = "Road Assistance"
    AUTOMOBILE_CLUB = "Automobile Club"
    RENTAL_CAR_AGENCY = "Rental Car Agency"
    TRUCK_SEMI_DEALER_SERVICES = "Truck-Semi Dealer-Services"
    TRUCK_DEALERSHIP = "Truck Dealership"
    TRUCK_PARKING = "Truck Parking"
    TRUCK_STOP_PLAZA = "Truck Stop-Plaza"
    TRUCK_WASH = "Truck Wash"
    HOSPITAL_OR_HEALTH_CARE_FACILITY = "Hospital or Health Care Facility"
    DENTIST_DENTAL_OFFICE = "Dentist-Dental Office"
    FAMILY_GENERAL_PRACTICE_PHYSICIANS = "Family-General Practice Physicians"
    PSYCHIATRIC_INSTITUTE = "Psychiatric Institute"
    NURSING_HOME = "Nursing Home"
    MEDICAL_SERVICES_CLINICS = "Medical Services-Clinics"
    HOSPITAL = "Hospital"
    OPTICAL = "Optical"
    VETERINARIAN = "Veterinarian"
    HOSPITAL_EMERGENCY_ROOM = "Hospital Emergency Room"
    THERAPIST = "Therapist"
    CHIROPRACTOR = "Chiropractor"
    BLOOD_BANK = "Blood Bank"
    COVID_19_TESTING_SITE = "COVID-19 Testing Site"
    GOVERNMENT_OR_COMMUNITY_FACILITY = "Government or Community Facility"
    CITY_HALL = "City Hall"
    EMBASSY = "Embassy"
    MILITARY_BASE = "Military Base"
    COUNTY_COUNCIL = "County Council"
    CIVIC_COMMUNITY_CENTER = "Civic-Community Center"
    COURT_HOUSE = "Court House"
    GOVERNMENT_OFFICE = "Government Office"
    BORDER_CROSSING = "Border Crossing"
    EDUCATION_FACILITY = "Education Facility"
    HIGHER_EDUCATION = "Higher Education"
    SCHOOL = "School"
    TRAINING_AND_DEVELOPMENT = "Training and Development"
    COACHING_INSTITUTE = "Coaching Institute"
    FINE_ARTS = "Fine Arts"
    LANGUAGE_STUDIES = "Language Studies"
    OTHER_LIBRARY = "Other Library"
    LIBRARY = "Library"
    EVENT_SPACES = "Event Spaces"
    BANQUET_HALL = "Banquet Hall"
    CONVENTION_EXHIBITION_CENTER = "Convention-Exhibition Center"
    PARKING = "Parking"
    PARKING_GARAGE_PARKING_HOUSE = "Parking Garage-Parking House"
    PARKING_LOT = "Parking Lot"
    PARK_AND_RIDE = "Park and Ride"
    MOTORCYCLE_MOPED_AND_SCOOTER_PARKING = "Motorcycle, Moped and Scooter Parking"
    CELLPHONE_PARKING_LOT = "Cellphone Parking Lot"
    SPORTS_FACILITY_VENUE = "Sports Facility-Venue"
    SPORTS_COMPLEX_STADIUM = "Sports Complex-Stadium"
    ICE_SKATING_RINK = "Ice Skating Rink"
    SWIMMING_POOL = "Swimming Pool"
    TENNIS_COURT = "Tennis Court"
    BOWLING_CENTER = "Bowling Center"
    INDOOR_SKI = "Indoor Ski"
    HOCKEY = "Hockey"
    RACQUETBALL_COURT = "Racquetball Court"
    SHOOTING_RANGE = "Shooting Range"
    SOCCER_CLUB = "Soccer Club"
    SQUASH_COURT = "Squash Court"
    FITNESS_HEALTH_CLUB = "Fitness-Health Club"
    INDOOR_SPORTS = "Indoor Sports"
    GOLF_COURSE = "Golf Course"
    GOLF_PRACTICE_RANGE = "Golf Practice Range"
    RACE_TRACK = "Race Track"
    SPORTING_INSTRUCTION_AND_CAMPS = "Sporting Instruction and Camps"
    SPORTS_ACTIVITIES = "Sports Activities"
    BASKETBALL = "Basketball"
    BADMINTON = "Badminton"
    RUGBY = "Rugby"
    DIVING_CENTER = "Diving Center"
    BIKE_PARK = "Bike Park"
    BMX_TRACK = "BMX Track"
    RUNNING_TRACK = "Running Track"
    FACILITIES = "Facilities"
    CEMETERY = "Cemetery"
    CREMATORIUM = "Crematorium"
    PUBLIC_RESTROOM_TOILETS = "Public Restroom-Toilets"
    CLUBHOUSE = "Clubhouse"
    REGISTRATION_OFFICE = "Registration Office"
    OUTDOOR_AREA_COMPLEX = "Outdoor Area-Complex"
    INDUSTRIAL_ZONE = "Industrial Zone"
    MARINA = "Marina"
    RV_PARKS = "RV Parks"
    COLLECTIVE_COMMUNITY = "Collective Community"
    ISLAND = "Island"
    MEETING_POINT = "Meeting Point"
    BUILDING = "Building"
    RESIDENTIAL_AREA_BUILDING = "Residential Area-Building"