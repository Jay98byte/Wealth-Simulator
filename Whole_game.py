import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageEnhance, ImageOps, ImageTk
import requests
from io import BytesIO
import base64
import json
import pickle
import random
import time
from pathlib import Path

# =========================================================
# GAME DATA
# =========================================================

balance = 0
total_clicks = 0
owned = []
passive_income_per_minute = 0

assets = {
    "Cars": [
        {
            "name": "Ferrari 296 GTB",
            "price": 338255,
            "image": "Assets/Cars/ferrari_296_gtb.jpg"
        },
        {
            "name": "Lamborghini Huracan",
            "price": 249000,
            "image": "Assets/Cars/Lamborghini_Huracan.jpg"
        },
        {
            "name": "Rolls-Royce Phantom",
            "price": 510000,
            "image": "Assets/Cars/rolls_royce_phantom.jpg"
        },
        {
            "name": "Bugatti Chiron",
            "price": 3300000,
            "image": "Assets/Cars/bugatti_chiron.jpg"
        }
    ],

    "Jets": [
        {
            "name": "Gulfstream G700",
            "price": 79900000,
            "image": "Assets/Jets/Gulfstream_G700.jpg"
        },
        {
            "name": "Bombardier Global 7500",
            "price": 75000000,
            "image": "Assets/Jets/Bombardier_Global_7500.jpg"
        }
    ],

    "Yachts": [
        {
            "name": "Azimut Grande",
            "price": 8500000,
            "image": "Assets/Yachts/Azimut_Grande.jpg"
        },
        {
            "name": "Heesen Yacht",
            "price": 50000000,
            "image": "Assets/Yachts/Heesen_Yacht.jpg"
        }
    ],

    "Businesses & Real Estate": [
        {
            "name": "Starter Apartment",
            "price": 170000,
            "income_per_minute": 35,
            "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Apartment_building.jpg"
        },
        {
            "name": "Downtown Office Building",
            "price": 8500000,
            "income_per_minute": 1800,
            "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Office_building.jpg"
        },
        {
            "name": "Independent Clothing Company",
            "price": 1200000,
            "income_per_minute": 240,
            "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Clothing_store.jpg"
        },
        {
            "name": "SaaS Software Company",
            "price": 5000000,
            "income_per_minute": 1400,
            "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Software_development.jpg"
        },
        {
            "name": "Broad Market Index Fund",
            "price": 60000,
            "income_per_minute": 12,
            "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Stock_market_display.jpg"
        }
    ]
}

assets["Jets"].extend([
    {"name": "Gulfstream G650ER", "price": 70000000, "image": "Assets/Jets/Gulfstream_G650ER.jpg"},
    {"name": "Dassault Falcon 8X", "price": 58000000, "image": "Assets/Jets/Dassault_Falcon_8X.jpg"},
    {"name": "Bombardier Challenger 650", "price": 33000000, "image": "Assets/Jets/Bombardier_Challenger_650.jpg"},
    {"name": "Embraer Praetor 600", "price": 21000000, "image": "Assets/Jets/Embraer_Praetor_600.jpg"},
    {"name": "Cessna Citation Longitude", "price": 28000000, "image": "Assets/Jets/Cessna_Citation_Longitude.jpg"},
    {"name": "Gulfstream G550", "price": 62000000, "image": "Assets/Jets/Gulfstream_G550.jpg"},
    {"name": "Embraer Legacy 650", "price": 26000000, "image": "Assets/Jets/Embraer_Legacy_650.jpg"},
    {"name": "Pilatus PC-24", "price": 12000000, "image": "Assets/Jets/Pilatus_PC_24.jpg"},
    {"name": "Airbus ACJ319", "price": 100000000, "image": "Assets/Jets/Airbus_ACJ319.jpg"},
    {"name": "HondaJet Elite II", "price": 7000000, "image": "Assets/Jets/HondaJet_Elite_II.jpg"},
])

assets["Yachts"].extend([
    {"name": "Lady Lau Superyacht", "price": 45000000, "image": "Assets/Yachts/Lady_Lau_Superyacht.jpg"},
    {"name": "Luxury Yacht", "price": 18000000, "image": "Assets/Yachts/Luxury_Yacht.jpg"},
    {"name": "Maldives Explorer", "price": 24000000, "image": "Assets/Yachts/Maldives_Explorer.jpg"},
    {"name": "Christina O", "price": 65000000, "image": "Assets/Yachts/Christina_O.jpg"},
    {"name": "Cranchi A46 Tender", "price": 1600000, "image": "Assets/Yachts/Cranchi_A46_Tender.jpg"},
    {"name": "Tango Superyacht", "price": 90000000, "image": "Assets/Yachts/Tango_Superyacht.jpg"},
    {"name": "Katara Superyacht", "price": 300000000, "image": "Assets/Yachts/Katara_Superyacht.jpg"},
    {"name": "Barcelona Luxury Yacht", "price": 22000000, "image": "Assets/Yachts/Barcelona_Luxury_Yacht.jpg"},
    {"name": "Saranda Luxury Yacht", "price": 14000000, "image": "Assets/Yachts/Saranda_Luxury_Yacht.jpg"},
    {"name": "Stella Maris", "price": 75000000, "image": "Assets/Yachts/Stella_Maris.jpg"},
])

assets["Cars"].extend([
    {"name": "Acura Integra", "price": 32600, "image": "Assets/Cars/acura_integra.jpg"},
    {"name": "Alfa Romeo Giulia", "price": 43350, "image": "Assets/Cars/alfa_romeo_giulia.jpg"},
    {"name": "Alfa Romeo Stelvio", "price": 47345, "image": "Assets/Cars/alfa_romeo_stelvio.jpg"},
    {"name": "Aston Martin DB12", "price": 245000, "image": "Assets/Cars/aston_martin_db12.jpg"},
    {"name": "Aston Martin Vantage", "price": 191000, "image": "Assets/Cars/aston_martin_vantage.jpg"},
    {"name": "Audi A4", "price": 41700, "image": "Assets/Cars/audi_a4.jpg"},
    {"name": "Audi A6", "price": 58200, "image": "Assets/Cars/audi_a6.jpg"},
    {"name": "Audi Q5", "price": 45700, "image": "Assets/Cars/audi_q5.jpg"},
    {"name": "Audi R8", "price": 158600, "image": "Assets/Cars/audi_r8.jpg"},
    {"name": "Audi RS 6 Avant", "price": 125800, "image": "Assets/Cars/audi_rs6_avant.jpg"},
    {"name": "BMW 3 Series", "price": 45900, "image": "Assets/Cars/bmw_3_series.jpg"},
    {"name": "BMW 5 Series", "price": 59200, "image": "Assets/Cars/bmw_5_series.jpg"},
    {"name": "BMW 7 Series", "price": 96800, "image": "Assets/Cars/bmw_7_series.jpg"},
    {"name": "BMW M2", "price": 64800, "image": "Assets/Cars/bmw_m2.jpg"},
    {"name": "BMW M4", "price": 80600, "image": "Assets/Cars/bmw_m4.jpg"},
    {"name": "BMW X5", "price": 66500, "image": "Assets/Cars/bmw_x5.jpg"},
    {"name": "Cadillac CT5-V Blackwing", "price": 95090, "image": "Assets/Cars/cadillac_ct5_v_blackwing.jpg"},
    {"name": "Cadillac Escalade", "price": 81895, "image": "Assets/Cars/cadillac_escalade.jpg"},
    {"name": "Chevrolet Camaro", "price": 32495, "image": "Assets/Cars/chevrolet_camaro.jpg"},
    {"name": "Chevrolet Corvette Stingray", "price": 68495, "image": "Assets/Cars/chevrolet_corvette_stingray.jpg"},
    {"name": "Chevrolet Tahoe", "price": 58800, "image": "Assets/Cars/chevrolet_tahoe.jpg"},
    {"name": "Dodge Challenger", "price": 32940, "image": "Assets/Cars/dodge_challenger.jpg"},
    {"name": "Dodge Charger", "price": 36970, "image": "Assets/Cars/dodge_charger.jpg"},
    {"name": "Dodge Durango SRT Hellcat", "price": 96295, "image": "Assets/Cars/dodge_durango_srt_hellcat.jpg"},
    {"name": "Ford Bronco", "price": 39390, "image": "Assets/Cars/ford_bronco.jpg"},
    {"name": "Ford F-150 Raptor", "price": 78700, "image": "Assets/Cars/ford_f150_raptor.jpg"},
    {"name": "Ford Mustang GT", "price": 44590, "image": "Assets/Cars/ford_mustang_gt.jpg"},
    {"name": "Ford Mustang Dark Horse", "price": 61165, "image": "Assets/Cars/ford_mustang_dark_horse.jpg"},
    {"name": "Genesis G80", "price": 54675, "image": "Assets/Cars/genesis_g80.jpg"},
    {"name": "Genesis GV80", "price": 75700, "image": "Assets/Cars/genesis_gv80.jpg"},
    {"name": "Honda Civic Type R", "price": 44950, "image": "Assets/Cars/honda_civic_type_r.jpg"},
    {"name": "Honda NSX", "price": 169500, "image": "Assets/Cars/honda_nsx.jpg"},
    {"name": "Hyundai Ioniq 5 N", "price": 66750, "image": "Assets/Cars/hyundai_ioniq_5_n.jpg"},
    {"name": "Infiniti QX80", "price": 82900, "image": "Assets/Cars/infiniti_qx80.jpg"},
    {"name": "Jaguar F-Type", "price": 77900, "image": "Assets/Cars/jaguar_f_type.jpg"},
    {"name": "Jaguar I-Pace", "price": 72100, "image": "Assets/Cars/jaguar_i_pace.jpg"},
    {"name": "Jeep Grand Cherokee", "price": 37710, "image": "Assets/Cars/jeep_grand_cherokee.jpg"},
    {"name": "Jeep Wrangler Rubicon", "price": 47895, "image": "Assets/Cars/jeep_wrangler_rubicon.jpg"},
    {"name": "Kia EV6 GT", "price": 62895, "image": "Assets/Cars/kia_ev6_gt.jpg"},
    {"name": "Koenigsegg Jesko", "price": 3000000, "image": "Assets/Cars/koenigsegg_jesko.jpg"},
    {"name": "Lamborghini Aventador", "price": 498000, "image": "Assets/Cars/lamborghini_aventador.jpg"},
    {"name": "Lamborghini Revuelto", "price": 608358, "image": "Assets/Cars/lamborghini_revuelto.jpg"},
    {"name": "Lamborghini Urus", "price": 249400, "image": "Assets/Cars/lamborghini_urus.jpg"},
    {"name": "Land Rover Defender", "price": 56900, "image": "Assets/Cars/land_rover_defender.jpg"},
    {"name": "Land Rover Range Rover", "price": 107400, "image": "Assets/Cars/range_rover.jpg"},
    {"name": "Lexus LC 500", "price": 100600, "image": "Assets/Cars/lexus_lc_500.jpg"},
    {"name": "Lexus LX 600", "price": 89160, "image": "Assets/Cars/lexus_lx_600.jpg"},
    {"name": "Lotus Emira", "price": 95900, "image": "Assets/Cars/lotus_emira.jpg"},
    {"name": "Maserati GranTurismo", "price": 174000, "image": "Assets/Cars/maserati_granturismo.jpg"},
    {"name": "Maserati MC20", "price": 217000, "image": "Assets/Cars/maserati_mc20.jpg"},
    {"name": "Mazda MX-5 Miata", "price": 28985, "image": "Assets/Cars/mazda_mx5_miata.jpg"},
    {"name": "McLaren 570S", "price": 192500, "image": "Assets/Cars/mclaren_570s.jpg"},
    {"name": "McLaren 750S", "price": 324000, "image": "Assets/Cars/mclaren_750s.jpg"},
    {"name": "McLaren Artura", "price": 237500, "image": "Assets/Cars/mclaren_artura.jpg"},
    {"name": "Mercedes-AMG GT", "price": 136050, "image": "Assets/Cars/mercedes_amg_gt.jpg"},
    {"name": "Mercedes-Benz S-Class", "price": 117750, "image": "Assets/Cars/mercedes_benz_s_class.jpg"},
    {"name": "Mercedes-Benz G-Class", "price": 143000, "image": "Assets/Cars/mercedes_benz_g_class.jpg"},
    {"name": "Mini Cooper JCW", "price": 38590, "image": "Assets/Cars/mini_cooper_jcw.jpg"},
    {"name": "Mitsubishi Lancer Evolution X", "price": 41600, "image": "Assets/Cars/mitsubishi_lancer_evolution_x.jpg"},
    {"name": "Nissan GT-R", "price": 121090, "image": "Assets/Cars/nissan_gtr.jpg"},
    {"name": "Nissan Z", "price": 43000, "image": "Assets/Cars/nissan_z.jpg"},
    {"name": "Pagani Huayra", "price": 2800000, "image": "Assets/Cars/pagani_huayra.jpg"},
    {"name": "Porsche 718 Cayman", "price": 68900, "image": "Assets/Cars/porsche_718_cayman.jpg"},
    {"name": "Porsche 911 Carrera", "price": 120100, "image": "Assets/Cars/porsche_911_carrera.jpg"},
    {"name": "Porsche 911 GT3", "price": 182900, "image": "Assets/Cars/porsche_911_gt3.jpg"},
    {"name": "Porsche Cayenne", "price": 79900, "image": "Assets/Cars/porsche_cayenne.jpg"},
    {"name": "Porsche Taycan Turbo S", "price": 209000, "image": "Assets/Cars/porsche_taycan_turbo_s.jpg"},
    {"name": "Ram 1500 TRX", "price": 96285, "image": "Assets/Cars/ram_1500_trx.jpg"},
    {"name": "Rivian R1T", "price": 69900, "image": "Assets/Cars/rivian_r1t.jpg"},
    {"name": "Rolls-Royce Cullinan", "price": 355000, "image": "Assets/Cars/rolls_royce_cullinan.jpg"},
    {"name": "Rolls-Royce Ghost", "price": 354750, "image": "Assets/Cars/rolls_royce_ghost.jpg"},
    {"name": "Shelby GT500", "price": 80400, "image": "Assets/Cars/shelby_gt500.jpg"},
    {"name": "Subaru WRX", "price": 32600, "image": "Assets/Cars/subaru_wrx.jpg"},
    {"name": "Tesla Model S Plaid", "price": 89990, "image": "Assets/Cars/tesla_model_s_plaid.jpg"},
    {"name": "Tesla Model X Plaid", "price": 99990, "image": "Assets/Cars/tesla_model_x_plaid.jpg"},
    {"name": "Toyota GR86", "price": 30100, "image": "Assets/Cars/toyota_gr86.jpg"},
    {"name": "Toyota GR Supra", "price": 55795, "image": "Assets/Cars/toyota_gr_supra.jpg"},
    {"name": "Toyota Land Cruiser", "price": 55400, "image": "Assets/Cars/toyota_land_cruiser.jpg"},
    {"name": "Toyota Tacoma TRD Pro", "price": 63400, "image": "Assets/Cars/toyota_tacoma_trd_pro.jpg"},
    {"name": "Toyota Tundra Capstone", "price": 78685, "image": "Assets/Cars/toyota_tundra_capstone.jpg"},
    {"name": "Volkswagen Golf R", "price": 45950, "image": "Assets/Cars/volkswagen_golf_r.jpg"},
    {"name": "Volvo XC90", "price": 57600, "image": "Assets/Cars/volvo_xc90.jpg"},
    {"name": "Acura MDX Type S", "price": 73350, "image": "Assets/Cars/acura_mdx_type_s.jpg"},
    {"name": "Bentley Bentayga", "price": 205250, "image": "Assets/Cars/bentley_bentayga.jpg"},
    {"name": "Bentley Continental GT", "price": 245425, "image": "Assets/Cars/bentley_continental_gt.jpg"},
    {"name": "Ferrari 488 GTB", "price": 262647, "image": "Assets/Cars/ferrari_488_gtb.jpg"},
    {"name": "Ferrari F8 Tributo", "price": 276550, "image": "Assets/Cars/ferrari_f8_tributo.jpg"},
    {"name": "Ferrari SF90 Stradale", "price": 528764, "image": "Assets/Cars/ferrari_sf90_stradale.jpg"},
    {"name": "Honda Civic Type R (FK8)", "price": 43400, "image": "Assets/Cars/honda_civic_type_r_fk8.jpg"},
    {"name": "Lexus RC F", "price": 68100, "image": "Assets/Cars/lexus_rc_f.jpg"},
    {"name": "Mercedes-AMG C 63", "price": 84900, "image": "Assets/Cars/mercedes_amg_c63.jpg"},
    {"name": "Nissan 370Z", "price": 30490, "image": "Assets/Cars/nissan_370z.jpg"},
    {"name": "Porsche Panamera", "price": 101550, "image": "Assets/Cars/porsche_panamera.jpg"},
    {"name": "Toyota GR Yaris", "price": 46600, "image": "Assets/Cars/toyota_gr_yaris.jpg"},
    {"name": "Volkswagen Golf GTI", "price": 31965, "image": "Assets/Cars/volkswagen_golf_gti.jpg"},
    {"name": "Volvo S90", "price": 58400, "image": "Assets/Cars/volvo_s90.jpg"},
    {"name": "Chevrolet Silverado ZR2", "price": 72600, "image": "Assets/Cars/chevrolet_silverado_zr2.jpg"},
    {"name": "Ford GT", "price": 500000, "image": "Assets/Cars/ford_gt.jpg"},
    {"name": "Hummer EV Pickup", "price": 97995, "image": "Assets/Cars/hummer_ev_pickup.jpg"},
    {"name": "Lucid Air Sapphire", "price": 249900, "image": "Assets/Cars/lucid_air_sapphire.jpg"},
])

assets["Real Estate"] = assets["Businesses & Real Estate"][:2]
assets["Businesses"] = assets["Businesses & Real Estate"][2:]

assets["Businesses"].extend([
    {
        "name": "Neighborhood Coffee Shop",
        "price": 85000,
        "income_per_minute": 38,
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Coffee_shop.jpg",
    },
    {
        "name": "Mobile Food Truck",
        "price": 125000,
        "income_per_minute": 55,
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Food_truck.jpg",
    },
    {
        "name": "Artisan Bakery",
        "price": 175000,
        "income_per_minute": 76,
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Bakery.jpg",
    },
    {
        "name": "Neighborhood Laundromat",
        "price": 260000,
        "income_per_minute": 115,
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Laundromat.jpg",
    },
    {
        "name": "Independent Bookstore",
        "price": 325000,
        "income_per_minute": 140,
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Bookshop.jpg",
    },
    {
        "name": "Pet Grooming Salon",
        "price": 390000,
        "income_per_minute": 170,
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Dog_grooming.jpg",
    },
    {
        "name": "Auto Repair Garage",
        "price": 575000,
        "income_per_minute": 250,
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Auto_repair_shop.jpg",
    },
    {
        "name": "Boutique Fitness Studio",
        "price": 725000,
        "income_per_minute": 315,
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Fitness_center.jpg",
    },
    {
        "name": "Family Restaurant",
        "price": 980000,
        "income_per_minute": 425,
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Restaurant.jpg",
    },
    {
        "name": "Small Boutique Hotel",
        "price": 1450000,
        "income_per_minute": 625,
        "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Boutique_hotel.jpg",
    },
])

assets["Real Estate"].extend([
    {"name": "Phoenix 3-Bedroom Ranch Home", "price": 365000, "image": "Assets/Real_Estate/phoenix_ranch_home.jpg"},
    {"name": "Cleveland Brick Bungalow", "price": 215000, "image": "Assets/Real_Estate/cleveland_bungalow.jpg"},
    {"name": "Columbus Starter Family Home", "price": 289000, "image": "Assets/Real_Estate/columbus_family_home.jpg"},
    {"name": "Indianapolis 4-Bedroom Home", "price": 325000, "image": "Assets/Real_Estate/indianapolis_family_home.jpg"},
    {"name": "Tucson Desert-Style Home", "price": 410000, "image": "Assets/Real_Estate/tucson_desert_home.jpg"},
    {"name": "Atlanta Townhouse", "price": 385000, "image": "Assets/Real_Estate/atlanta_townhouse.jpg"},
    {"name": "Charlotte 4-Bedroom Home", "price": 525000, "image": "Assets/Real_Estate/charlotte_family_home.jpg"},
    {"name": "Dallas Suburban Home", "price": 475000, "image": "Assets/Real_Estate/dallas_suburban_home.jpg"},
    {"name": "Denver Mountain-View Home", "price": 780000, "image": "Assets/Real_Estate/denver_mountain_home.jpg"},
    {"name": "Seattle Craftsman Home", "price": 925000, "image": "Assets/Real_Estate/seattle_craftsman_home.jpg"},
    {"name": "Portland Craftsman House", "price": 625000, "image": "Assets/Real_Estate/portland_craftsman_home.jpg"},
    {"name": "Nashville Family Home", "price": 560000, "image": "Assets/Real_Estate/nashville_family_home.jpg"},
    {"name": "Tampa Waterfront Home", "price": 875000, "image": "Assets/Real_Estate/tampa_waterfront_home.jpg"},
    {"name": "Orlando 4-Bedroom Home", "price": 495000, "image": "Assets/Real_Estate/orlando_family_home.jpg"},
    {"name": "Raleigh Modern Home", "price": 515000, "image": "Assets/Real_Estate/raleigh_modern_home.jpg"},
    {"name": "Minneapolis 4-Bedroom Home", "price": 445000, "image": "Assets/Real_Estate/minneapolis_family_home.jpg"},
    {"name": "Detroit Brick Colonial Home", "price": 275000, "image": "Assets/Real_Estate/detroit_brick_home.jpg"},
    {"name": "Boise Foothills Home", "price": 599000, "image": "Assets/Real_Estate/boise_foothills_home.jpg"},
    {"name": "San Antonio Stucco Home", "price": 325000, "image": "Assets/Real_Estate/san_antonio_stucco_home.jpg"},
    {"name": "Sacramento Family Home", "price": 625000, "image": "Assets/Real_Estate/sacramento_family_home.jpg"},
    {"name": "New York Studio Condo", "price": 575000, "image": "Assets/Real_Estate/new_york_studio_condo.jpg"},
    {"name": "Chicago Loft Condo", "price": 425000, "image": "Assets/Real_Estate/chicago_loft_condo.jpg"},
    {"name": "Miami High-Rise Condo", "price": 825000, "image": "Assets/Real_Estate/miami_highrise_condo.jpg"},
    {"name": "San Francisco One-Bedroom Condo", "price": 1150000, "image": "Assets/Real_Estate/san_francisco_condo.jpg"},
    {"name": "Los Angeles Condo", "price": 765000, "image": "Assets/Real_Estate/los_angeles_condo.jpg"},
    {"name": "Boston Brownstone Condo", "price": 895000, "image": "Assets/Real_Estate/boston_brownstone_condo.jpg"},
    {"name": "Washington DC Condo", "price": 685000, "image": "Assets/Real_Estate/washington_dc_condo.jpg"},
    {"name": "Austin Downtown Condo", "price": 450000, "image": "Assets/Real_Estate/austin_downtown_condo.jpg"},
    {"name": "Honolulu Ocean-View Condo", "price": 775000, "image": "Assets/Real_Estate/honolulu_condo.jpg"},
    {"name": "Jersey City Luxury Condo", "price": 950000, "image": "Assets/Real_Estate/jersey_city_condo.jpg"},
    {"name": "Brooklyn Brownstone", "price": 2400000, "image": "Assets/Real_Estate/brooklyn_brownstone.jpg"},
    {"name": "San Diego Oceanfront Condo", "price": 1800000, "image": "Assets/Real_Estate/san_diego_oceanfront_condo.jpg"},
    {"name": "Manhattan Penthouse", "price": 8500000, "image": "Assets/Real_Estate/manhattan_penthouse.jpg"},
    {"name": "Aspen Ski Chalet", "price": 5200000, "image": "Assets/Real_Estate/aspen_ski_chalet.jpg"},
    {"name": "Malibu Beach House", "price": 6800000, "image": "Assets/Real_Estate/malibu_beach_house.jpg"},
    {"name": "Hamptons Estate", "price": 9500000, "image": "Assets/Real_Estate/hamptons_estate.jpg"},
    {"name": "Beverly Hills Mansion", "price": 12500000, "image": "Assets/Real_Estate/beverly_hills_mansion.jpg"},
    {"name": "Scottsdale Desert Estate", "price": 3200000, "image": "Assets/Real_Estate/scottsdale_estate.jpg"},
    {"name": "Lake Tahoe Lodge", "price": 3800000, "image": "Assets/Real_Estate/lake_tahoe_lodge.jpg"},
    {"name": "Napa Valley Vineyard Estate", "price": 7400000, "image": "Assets/Real_Estate/napa_vineyard_estate.jpg"},
    {"name": "Houston Mid-Rise Apartments", "price": 6500000, "image": "Assets/Real_Estate/houston_apartment_building.jpg"},
    {"name": "Phoenix Apartment Complex", "price": 4800000, "image": "Assets/Real_Estate/phoenix_apartment_complex.jpg"},
    {"name": "Atlanta 12-Unit Apartment Building", "price": 3500000, "image": "Assets/Real_Estate/atlanta_apartment_building.jpg"},
    {"name": "Denver 8-Unit Apartment Building", "price": 4300000, "image": "Assets/Real_Estate/denver_apartment_building.jpg"},
    {"name": "Seattle 6-Unit Apartment Building", "price": 3900000, "image": "Assets/Real_Estate/seattle_apartment_building.jpg"},
    {"name": "Brooklyn 4-Unit Apartment Building", "price": 2800000, "image": "Assets/Real_Estate/brooklyn_apartment_building.jpg"},
    {"name": "Chicago 20-Unit Apartment Building", "price": 5200000, "image": "Assets/Real_Estate/chicago_apartment_building.jpg"},
    {"name": "Miami Luxury Apartment Tower", "price": 18000000, "image": "Assets/Real_Estate/miami_apartment_tower.jpg"},
    {"name": "Austin Apartment Community", "price": 7500000, "image": "Assets/Real_Estate/austin_apartment_complex.jpg"},
    {"name": "Portland Apartment Building", "price": 4600000, "image": "Assets/Real_Estate/portland_apartment_building.jpg"},
    {"name": "Manhattan Boutique Hotel", "price": 28000000, "image": "Assets/Real_Estate/manhattan_boutique_hotel.jpg"},
    {"name": "Colorado Mountain Ski Resort", "price": 35000000, "image": "Assets/Real_Estate/colorado_ski_resort.jpg"},
    {"name": "Florida Beachfront Resort", "price": 42000000, "image": "Assets/Real_Estate/florida_beach_resort.jpg"},
    {"name": "Southwest Roadside Motel", "price": 2600000, "image": "Assets/Real_Estate/roadside_motel.jpg"},
    {"name": "London Georgian Townhouse", "price": 2300000, "image": "Assets/Real_Estate/london_townhouse.jpg"},
    {"name": "Paris Haussmann Apartment", "price": 1200000, "image": "Assets/Real_Estate/paris_apartment.jpg"},
    {"name": "Tuscany Country Villa", "price": 3500000, "image": "Assets/Real_Estate/tuscany_villa.jpg"},
    {"name": "French Riviera Villa", "price": 8800000, "image": "Assets/Real_Estate/french_riviera_villa.jpg"},
    {"name": "Swiss Alpine Chalet", "price": 4200000, "image": "Assets/Real_Estate/swiss_alpine_chalet.jpg"},
    {"name": "Barcelona Penthouse", "price": 2700000, "image": "Assets/Real_Estate/barcelona_penthouse.jpg"},
    {"name": "Tokyo City Apartment", "price": 1100000, "image": "Assets/Real_Estate/tokyo_apartment.jpg"},
    {"name": "Singapore Luxury Condo", "price": 2400000, "image": "Assets/Real_Estate/singapore_condo.jpg"},
    {"name": "Dubai Marina Penthouse", "price": 6000000, "image": "Assets/Real_Estate/dubai_penthouse.jpg"},
    {"name": "Sydney Harbour Apartment", "price": 2900000, "image": "Assets/Real_Estate/sydney_harbour_apartment.jpg"},
    {"name": "New Zealand Coastal Home", "price": 1400000, "image": "Assets/Real_Estate/new_zealand_coastal_home.jpg"},
    {"name": "Bali Private Villa", "price": 1100000, "image": "Assets/Real_Estate/bali_villa.jpg"},
    {"name": "Phuket Resort Villa", "price": 1600000, "image": "Assets/Real_Estate/phuket_villa.jpg"},
    {"name": "Costa Rica Eco-Lodge", "price": 1800000, "image": "Assets/Real_Estate/costa_rica_eco_lodge.jpg"},
    {"name": "Mexico City Condominio", "price": 425000, "image": "Assets/Real_Estate/mexico_city_condo.jpg"},
    {"name": "Vancouver Townhouse", "price": 1700000, "image": "Assets/Real_Estate/vancouver_townhouse.jpg"},
    {"name": "Iowa 320-Acre Grain Farm", "price": 2000000, "image": "Assets/Real_Estate/iowa_grain_farm.jpg"},
    {"name": "Texas Cattle Ranch", "price": 12000000, "image": "Assets/Real_Estate/texas_cattle_ranch.jpg"},
    {"name": "Montana Working Ranch", "price": 18000000, "image": "Assets/Real_Estate/montana_ranch.jpg"},
    {"name": "Sonoma County Vineyard", "price": 6500000, "image": "Assets/Real_Estate/sonoma_vineyard.jpg"},
    {"name": "Florida Citrus Grove", "price": 4100000, "image": "Assets/Real_Estate/florida_citrus_grove.jpg"},
    {"name": "Colorado Horse Ranch", "price": 7800000, "image": "Assets/Real_Estate/colorado_horse_ranch.jpg"},
    {"name": "Midwest Grain Farm", "price": 3500000, "image": "Assets/Real_Estate/midwest_grain_farm.jpg"},
    {"name": "Oregon Timberland", "price": 2800000, "image": "Assets/Real_Estate/oregon_timberland.jpg"},
    {"name": "Wyoming Cattle Ranch", "price": 9700000, "image": "Assets/Real_Estate/wyoming_ranch.jpg"},
    {"name": "California Almond Orchard", "price": 5200000, "image": "Assets/Real_Estate/california_orchard.jpg"},
    {"name": "Downtown Office Tower", "price": 14500000, "image": "Assets/Real_Estate/downtown_office_tower.jpg"},
    {"name": "Suburban Office Campus", "price": 22000000, "image": "Assets/Real_Estate/suburban_office_campus.jpg"},
    {"name": "Urban Coworking Building", "price": 9200000, "image": "Assets/Real_Estate/coworking_building.jpg"},
    {"name": "Medical Office Building", "price": 5800000, "image": "Assets/Real_Estate/medical_office_building.jpg"},
    {"name": "Regional Logistics Warehouse", "price": 8600000, "image": "Assets/Real_Estate/logistics_warehouse.jpg"},
    {"name": "Distribution Center", "price": 28000000, "image": "Assets/Real_Estate/distribution_center.jpg"},
    {"name": "Urban Retail Center", "price": 12000000, "image": "Assets/Real_Estate/urban_retail_center.jpg"},
    {"name": "Neighborhood Shopping Center", "price": 10000000, "image": "Assets/Real_Estate/neighborhood_shopping_center.jpg"},
    {"name": "Grocery-Anchored Shopping Plaza", "price": 16000000, "image": "Assets/Real_Estate/grocery_shopping_plaza.jpg"},
    {"name": "Industrial Flex Facility", "price": 7400000, "image": "Assets/Real_Estate/industrial_flex_facility.jpg"},
    {"name": "Self-Storage Facility", "price": 5500000, "image": "Assets/Real_Estate/self_storage_facility.jpg"},
    {"name": "Commercial Car Wash", "price": 1800000, "image": "Assets/Real_Estate/commercial_car_wash.jpg"},
    {"name": "Neighborhood Strip Mall", "price": 3200000, "image": "Assets/Real_Estate/strip_mall.jpg"},
    {"name": "Hyperscale Data Center", "price": 48000000, "image": "Assets/Real_Estate/data_center.jpg"},
    {"name": "Downtown Parking Garage", "price": 6300000, "image": "Assets/Real_Estate/parking_garage.jpg"},
    {"name": "Mixed-Use High-Rise", "price": 37000000, "image": "Assets/Real_Estate/mixed_use_highrise.jpg"},
    {"name": "Waterfront Development Parcel", "price": 3500000, "image": "Assets/Real_Estate/waterfront_land.jpg"},
    {"name": "Downtown Development Lot", "price": 8700000, "image": "Assets/Real_Estate/downtown_development_land.jpg"},
    {"name": "Rocky Mountain Vacation Cabin", "price": 625000, "image": "Assets/Real_Estate/mountain_cabin.jpg"},
    {"name": "Palm Springs Desert Vacation Home", "price": 725000, "image": "Assets/Real_Estate/desert_vacation_home.jpg"},
])

for property_asset in assets["Real Estate"][2:]:
    property_asset["income_per_minute"] = round(property_asset["price"] * 0.00021, 2)


# =========================================================
# STOCK MARKET
# =========================================================

SAVE_FILE = str(Path(__file__).with_name("wealth_clicker_save.json"))


class Stock:
    """One independent price process with its own RNG and market state."""

    def __init__(
        self, name, symbol, starting_price, minimum_price, maximum_price,
        volatility, trend, speed, momentum_strength, mean_reversion, seed
    ):
        self.name = name
        self.symbol = symbol
        self.starting_price = starting_price
        self.minimum_price = minimum_price
        self.maximum_price = maximum_price
        self.volatility = volatility
        self.trend = trend
        self.speed = speed
        self.momentum_strength = momentum_strength
        self.mean_reversion = mean_reversion
        self.seed = seed
        self.rng = random.Random(seed)
        self.price = starting_price
        self.momentum = 0.0
        self.temporary_bias = 0.0
        self.event_ticks_remaining = 0
        self.event_volatility = 1.0
        self.current_trend = 0.0
        self.trend_ticks_remaining = 0
        self.history = [starting_price]

    def update(self):
        if self.trend_ticks_remaining <= 0:
            direction = self.rng.choice((-1, 1))
            self.current_trend = direction * self.rng.uniform(
                0.00015, self.trend
            )
            self.trend_ticks_remaining = self.rng.randint(6, 18)
        self.trend_ticks_remaining -= 1

        noise = self.rng.gauss(0, self.volatility) * self.speed
        self.momentum = (
            self.momentum * 0.55 + noise * self.momentum_strength
        )
        reversion = (
            (self.starting_price - self.price) / self.starting_price
            * self.mean_reversion * self.speed * self.price
        )
        trend_move = self.current_trend * self.speed * self.price
        event_move = self.temporary_bias * self.speed * self.price

        if self.event_ticks_remaining > 0:
            self.event_ticks_remaining -= 1
            if self.event_ticks_remaining == 0:
                self.temporary_bias = 0
                self.event_volatility = 1.0
        elif self.rng.random() < 0.003:
            direction = 1 if self.rng.random() > 0.5 else -1
            self.temporary_bias = direction * self.rng.uniform(0.0005, 0.0015)
            self.event_ticks_remaining = self.rng.randint(3, 8)
            self.event_volatility = self.rng.uniform(1.2, 1.8)
            event_move += self.price * direction * self.rng.uniform(0.01, 0.025)

        change = (
            noise * self.event_volatility
            + self.momentum
            + trend_move
            + reversion
            + event_move
        )
        self.price = max(
            self.minimum_price,
            min(self.maximum_price, self.price + change)
        )
        self.history.append(round(self.price, 2))
        self.history = self.history[-120:]

    def to_dict(self):
        random_state = base64.b64encode(
            pickle.dumps(self.rng.getstate())
        ).decode("ascii")
        return {
            "price": self.price,
            "momentum": self.momentum,
            "temporary_bias": self.temporary_bias,
            "event_ticks_remaining": self.event_ticks_remaining,
            "event_volatility": self.event_volatility,
            "current_trend": self.current_trend,
            "trend_ticks_remaining": self.trend_ticks_remaining,
            "history": self.history,
            "random_state": random_state,
        }

    def load_dict(self, data):
        self.price = max(
            self.minimum_price,
            min(self.maximum_price, data.get("price", self.starting_price))
        )
        self.momentum = data.get("momentum", 0.0)
        self.temporary_bias = data.get("temporary_bias", 0.0)
        self.event_ticks_remaining = data.get("event_ticks_remaining", 0)
        self.event_volatility = data.get("event_volatility", 1.0)
        self.current_trend = data.get("current_trend", 0.0)
        self.trend_ticks_remaining = data.get("trend_ticks_remaining", 0)
        saved_history = data.get("history", [self.price])[-120:]
        self.history = [
            round(
                max(self.minimum_price, min(self.maximum_price, price)),
                2
            )
            for price in saved_history
        ]
        if not self.history:
            self.history = [self.price]
        if data.get("random_state"):
            state = pickle.loads(base64.b64decode(data["random_state"]))
            self.rng.setstate(state)


class StockMarket:
    def __init__(self, definitions):
        self.stocks = {
            definition["symbol"]: Stock(**definition)
            for definition in definitions
        }

    def update(self):
        for stock in self.stocks.values():
            stock.update()

    def to_dict(self):
        return {symbol: stock.to_dict() for symbol, stock in self.stocks.items()}

    def load_dict(self, data):
        for symbol, stock_data in data.items():
            if symbol in self.stocks:
                self.stocks[symbol].load_dict(stock_data)


class Portfolio:
    def __init__(self, cash=0):
        self.cash = cash
        self.holdings = {}

    def buy(self, stock, quantity):
        cost = stock.price * quantity
        if quantity < 1 or self.cash < cost:
            return False
        holding = self.holdings.setdefault(
            stock.symbol, {"quantity": 0, "average_price": 0.0}
        )
        total_cost = (
            holding["average_price"] * holding["quantity"] + cost
        )
        holding["quantity"] += quantity
        holding["average_price"] = total_cost / holding["quantity"]
        self.cash -= cost
        return True

    def sell(self, stock, quantity):
        holding = self.holdings.get(stock.symbol)
        if not holding or quantity < 1 or holding["quantity"] < quantity:
            return None
        realized = (
            stock.price - holding["average_price"]
        ) * quantity
        holding["quantity"] -= quantity
        self.cash += stock.price * quantity
        if holding["quantity"] == 0:
            del self.holdings[stock.symbol]
        return realized

    def to_dict(self):
        return {"cash": self.cash, "holdings": self.holdings}

    def load_dict(self, data):
        self.cash = data.get("cash", self.cash)
        self.holdings = data.get("holdings", {})


stock_definitions = [
    {"name": "TechNova", "symbol": "TNVA", "starting_price": 128, "minimum_price": 25, "maximum_price": 50, "volatility": 2.8, "trend": 0.0010, "speed": 0.8, "momentum_strength": 0.7, "mean_reversion": 0.10, "seed": 141},
    {"name": "MegaBank", "symbol": "MBNK", "starting_price": 92, "minimum_price": 40, "maximum_price": 60, "volatility": 0.65, "trend": 0.0002, "speed": 0.45, "momentum_strength": 0.35, "mean_reversion": 0.28, "seed": 287},
    {"name": "AutoWorks", "symbol": "AUTO", "starting_price": 76, "minimum_price": 18, "maximum_price": 80, "volatility": 1.8, "trend": -0.0002, "speed": 0.65, "momentum_strength": 0.55, "mean_reversion": 0.16, "seed": 394},
    {"name": "BioGen Labs", "symbol": "BIOG", "starting_price": 214, "minimum_price": 12, "maximum_price": 30, "volatility": 5.5, "trend": 0.0003, "speed": 0.9, "momentum_strength": 0.85, "mean_reversion": 0.06, "seed": 509},
    {"name": "RetailMax", "symbol": "RTMX", "starting_price": 54, "minimum_price": 20, "maximum_price": 50, "volatility": 0.85, "trend": 0.0001, "speed": 0.38, "momentum_strength": 0.4, "mean_reversion": 0.24, "seed": 613},
    {"name": "GreenGrid Energy", "symbol": "GRID", "starting_price": 67, "minimum_price": 15, "maximum_price": 40, "volatility": 2.4, "trend": 0.0007, "speed": 0.72, "momentum_strength": 0.65, "mean_reversion": 0.11, "seed": 727},
    {"name": "CloudCore", "symbol": "CLCR", "starting_price": 183, "minimum_price": 30, "maximum_price": 60, "volatility": 3.7, "trend": 0.0012, "speed": 0.86, "momentum_strength": 0.76, "mean_reversion": 0.07, "seed": 839},
    {"name": "Oceanic Freight", "symbol": "OCFR", "starting_price": 41, "minimum_price": 9, "maximum_price": 20, "volatility": 1.5, "trend": -0.0004, "speed": 0.58, "momentum_strength": 0.5, "mean_reversion": 0.19, "seed": 947},
    {"name": "AeroSpace United", "symbol": "AERO", "starting_price": 145, "minimum_price": 35, "maximum_price": 70, "volatility": 2.9, "trend": 0.0005, "speed": 0.68, "momentum_strength": 0.6, "mean_reversion": 0.12, "seed": 1051},
    {"name": "PharmaFirst", "symbol": "PHRM", "starting_price": 111, "minimum_price": 28, "maximum_price": 50, "volatility": 1.25, "trend": 0.0004, "speed": 0.5, "momentum_strength": 0.44, "mean_reversion": 0.20, "seed": 1163},
    {"name": "QuantumForge", "symbol": "QFRG", "starting_price": 305, "minimum_price": 8, "maximum_price": 20, "volatility": 7.0, "trend": 0.0015, "speed": 0.95, "momentum_strength": 0.92, "mean_reversion": 0.04, "seed": 1277},
    {"name": "Harvest Foods", "symbol": "HFD", "starting_price": 38, "minimum_price": 17, "maximum_price": 30, "volatility": 0.55, "trend": 0.0001, "speed": 0.32, "momentum_strength": 0.3, "mean_reversion": 0.32, "seed": 1381},
    {"name": "MetroBuild", "symbol": "MTBL", "starting_price": 83, "minimum_price": 22, "maximum_price": 33, "volatility": 1.9, "trend": -0.0001, "speed": 0.62, "momentum_strength": 0.52, "mean_reversion": 0.18, "seed": 1493},
    {"name": "StreamWave Media", "symbol": "SWAV", "starting_price": 61, "minimum_price": 10, "maximum_price": 40, "volatility": 3.4, "trend": 0.0008, "speed": 0.84, "momentum_strength": 0.8, "mean_reversion": 0.08, "seed": 1511},
    {"name": "Silverline Mining", "symbol": "SLVM", "starting_price": 97, "minimum_price": 25, "maximum_price": 60, "volatility": 2.2, "trend": -0.0003, "speed": 0.7, "momentum_strength": 0.58, "mean_reversion": 0.14, "seed": 1627},
    {"name": "SecureNet", "symbol": "SCNT", "starting_price": 156, "minimum_price": 450, "maximum_price": 850, "volatility": 2.0, "trend": 0.0009, "speed": 0.66, "momentum_strength": 0.62, "mean_reversion": 0.10, "seed": 1739},
    {"name": "TravelSphere", "symbol": "TRSP", "starting_price": 48, "minimum_price": 120, "maximum_price": 250, "volatility": 2.6, "trend": 0.0002, "speed": 0.78, "momentum_strength": 0.7, "mean_reversion": 0.13, "seed": 1847},
    {"name": "WaterWorks", "symbol": "WTRW", "starting_price": 72, "minimum_price": 100, "maximum_price": 190, "volatility": 0.7, "trend": 0.0003, "speed": 0.4, "momentum_strength": 0.36, "mean_reversion": 0.29, "seed": 1951},
    {"name": "LuxuryHouse", "symbol": "LUXH", "starting_price": 235, "minimum_price": 700, "maximum_price": 1000, "volatility": 4.1, "trend": 0.0006, "speed": 0.82, "momentum_strength": 0.72, "mean_reversion": 0.09, "seed": 2063},
    {"name": "DataHarbor", "symbol": "DHRB", "starting_price": 119, "minimum_price": 400, "maximum_price": 720, "volatility": 3.0, "trend": 0.0005, "speed": 0.74, "momentum_strength": 0.67, "mean_reversion": 0.10, "seed": 2179},
]


def calibrate_stock_definitions(definitions):
    """Apply narrow, mean-reverting price bands and modest market movement."""
    for definition in definitions:
        starting_price = definition["starting_price"]
        minimum_price = starting_price * 0.85
        maximum_price = starting_price * 1.15
        price_range = maximum_price - minimum_price
        definition["minimum_price"] = round(max(1, minimum_price), 2)
        definition["maximum_price"] = round(maximum_price, 2)
        definition["volatility"] = round(price_range * 0.02, 2)
        definition["trend"] = 0.0008
        definition["speed"] = 0.35
        definition["momentum_strength"] = 0.3
        definition["mean_reversion"] = 0.3


calibrate_stock_definitions(stock_definitions)
stock_market = StockMarket(stock_definitions)
portfolio = Portfolio(balance)


def load_game_state():
    global balance, owned, passive_income_per_minute
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as save_file:
            data = json.load(save_file)
        stock_market.load_dict(data.get("market", {}))
        portfolio.load_dict(data.get("portfolio", {}))
        balance = portfolio.cash
        owned = data.get("owned", [])
        passive_income_per_minute = data.get("passive_income_per_minute", 0)
        saved_at = data.get("saved_at")
        if saved_at is not None:
            try:
                elapsed_seconds = max(0, time.time() - float(saved_at))
            except (TypeError, ValueError):
                elapsed_seconds = 0
            balance += passive_income_per_minute * elapsed_seconds / 60
            portfolio.cash = balance
    except (FileNotFoundError, json.JSONDecodeError, ValueError, KeyError):
        portfolio.cash = balance


def save_game_state():
    portfolio.cash = balance
    with open(SAVE_FILE, "w", encoding="utf-8") as save_file:
        json.dump({
            "balance": balance,
            "owned": owned,
            "passive_income_per_minute": passive_income_per_minute,
            "market": stock_market.to_dict(),
            "portfolio": portfolio.to_dict(),
            "saved_at": time.time(),
        }, save_file)


load_game_state()
save_game_state()


# =========================================================
# WINDOW
# =========================================================

root = tk.Tk()
root.title("💰 Wealth Clicker")
root.geometry("1200x750")
root.configure(bg="#07111f")


# =========================================================
# COLORS
# =========================================================

BG = "#07111f"
PANEL = "#0d1b2a"
GREEN = "#00e676"
WHITE = "#ffffff"
GRAY = "#8fa3b8"
RED = "#ff5252"


# =========================================================
# VARIABLES
# =========================================================

balance_text = tk.StringVar(value="$0")
click_text = tk.StringVar(value="Clicks: 0")
owned_text = tk.StringVar(value="Assets Owned: 0")


# =========================================================
# FUNCTIONS
# =========================================================

BUTTON_BASE_BG = "#13263a"
BUTTON_HOVER_BG = "#edf4ff"
BUTTON_CLICK_BG = "#ffffff"
BUTTON_TEXT_LIGHT = "#ffffff"
BUTTON_TEXT_DARK = "#07111f"
BUTTON_ACTIVE_BG = GREEN
BUTTON_ACTIVE_FG = "black"


def style_button(button, default_bg=BUTTON_BASE_BG, default_fg=BUTTON_TEXT_LIGHT,
                 selected_bg=BUTTON_ACTIVE_BG, selected_fg=BUTTON_ACTIVE_FG,
                 hover_bg=BUTTON_HOVER_BG, click_bg=BUTTON_CLICK_BG,
                 click_fg=BUTTON_TEXT_DARK):
    button.config(
        bg=default_bg,
        fg=default_fg,
        activebackground=click_bg,
        activeforeground=click_fg,
        relief="flat",
        highlightthickness=0,
        bd=0,
    )
    button._selected = False
    button._pressed = False

    def on_enter(event):
        if button._pressed:
            button.config(bg=click_bg, fg=click_fg)
        elif button._selected:
            button.config(bg=selected_bg, fg=selected_fg)
        else:
            button.config(bg=hover_bg, fg=BUTTON_TEXT_DARK)

    def on_leave(event):
        if button._selected:
            button.config(bg=selected_bg, fg=selected_fg)
        else:
            button.config(bg=default_bg, fg=default_fg)

    def on_press(event):
        button._pressed = True
        button.config(bg=click_bg, fg=click_fg)

    def on_release(event):
        button._pressed = False
        if button._selected:
            button.config(bg=selected_bg, fg=selected_fg)
        else:
            button.config(bg=default_bg, fg=default_fg)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.bind("<ButtonPress-1>", on_press)
    button.bind("<ButtonRelease-1>", on_release)
    return button


def make_button(parent, text, command=None, *, selected=False,
                default_bg=BUTTON_BASE_BG, default_fg=BUTTON_TEXT_LIGHT,
                selected_bg=BUTTON_ACTIVE_BG, selected_fg=BUTTON_ACTIVE_FG):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 12, "bold"),
        bg=selected_bg if selected else default_bg,
        fg=selected_fg if selected else default_fg,
        relief="flat",
        padx=10,
        pady=6,
    )
    button._selected = bool(selected)
    style_button(
        button,
        default_bg=default_bg,
        default_fg=default_fg,
        selected_bg=selected_bg,
        selected_fg=selected_fg,
    )
    button._selected = bool(selected)
    if selected:
        button.config(bg=selected_bg, fg=selected_fg)
    return button


def set_button_selected(button, selected, default_bg=BUTTON_BASE_BG,
                        default_fg=BUTTON_TEXT_LIGHT,
                        selected_bg=BUTTON_ACTIVE_BG,
                        selected_fg=BUTTON_ACTIVE_FG):
    if button is None:
        return
    button._selected = bool(selected)
    button.config(
        bg=selected_bg if selected else default_bg,
        fg=selected_fg if selected else default_fg
    )


def update_screen():
    balance_label.config(text=f"${balance:,.2f}")
    income_label.config(text=f"Passive income: ${passive_income_per_minute:,.2f}/min")
    portfolio.cash = balance


def floating_money(amount, x, y, color=GREEN):
    """Creates animated floating money text."""

    text = tk.Label(
        root,
        text=f"+${amount}" if amount > 0 else f"-${abs(amount)}",
        font=("Arial", 20, "bold"),
        bg=BG,
        fg=color
    )

    text.place(x=x, y=y)

    def animate(step=0):
        if step < 25:
            text.place(x=x, y=y - step * 3)
            root.after(30, lambda: animate(step + 1))
        else:
            text.destroy()

    animate()


def earn_money():
    global balance, total_clicks

    balance += 1
    total_clicks += 1

    update_screen()

    # Animation near the money button
    floating_money(
        1,
        money_button.winfo_rootx() - root.winfo_rootx() + 70,
        money_button.winfo_rooty() - root.winfo_rooty()
    )


def buy_asset(asset, purchase_price=None, upgrade_option=None, upgrade_type=None):
    global balance, passive_income_per_minute

    if purchase_price is None:
        purchase_price = asset["price"]

    if asset["name"] in owned:
        messagebox.showinfo(
            "Already Owned",
            f"You already own {asset['name']}."
        )
        return

    if balance >= purchase_price:

        balance -= purchase_price
        owned.append(asset["name"])
        passive_income_per_minute += asset.get("income_per_minute", 0)

        update_screen()

        floating_money(
            -purchase_price,
            root.winfo_width() // 2,
            150,
            RED
        )

        messagebox.showinfo(
            "Purchase Complete 🎉",
            f"You bought a {asset['name']}"
            f"{f' with the {upgrade_option} {upgrade_type}' if upgrade_option else ''}!\n"
            f"Income: ${asset.get('income_per_minute', 0):,.2f} per minute"
        )
        show_page(current_page)

    else:
        messagebox.showwarning(
            "Not Enough Money 💸",
            f"You need ${purchase_price:,.2f}.\n\n"
            f"Your balance: ${balance:,.2f}"
        )


def collect_passive_income():
    """Credit purchased business and property income every second."""
    global balance

    if passive_income_per_minute:
        balance += passive_income_per_minute / 60
        update_screen()

    root.after(1000, collect_passive_income)


selected_stock_symbol = "TNVA"
stock_chart_canvas = None
stock_list_body = None
stock_price_label = None
stock_position_label = None
stock_quantity_var = None
stock_detail_frame = None
home_earning_frame = None
home_investing_frame = None
home_investing_content = None
home_investing_buttons = {}
navigation_buttons = {}
active_investing_mode = "real_estate"


def selected_stock():
    return stock_market.stocks[selected_stock_symbol]


def format_money(value):
    return f"${value:,.2f}"


def refresh_stock_chart():
    if stock_chart_canvas is None:
        return
    stock = selected_stock()
    stock_chart_canvas.delete("all")
    width = max(stock_chart_canvas.winfo_width(), 420)
    height = max(stock_chart_canvas.winfo_height(), 190)
    history = stock.history
    low = min(history)
    high = max(history)
    price_range = max(high - low, 1)
    points = []
    for index, price in enumerate(history):
        x = 12 + (width - 24) * index / max(len(history) - 1, 1)
        y = height - 18 - (height - 32) * (price - low) / price_range
        points.extend((x, y))
    if len(points) >= 4:
        area_points = [points[0], height - 18] + points + [
            points[-2], height - 18
        ]
        stock_chart_canvas.create_polygon(
            area_points, fill="#0b5c43", outline=""
        )
        stock_chart_canvas.create_line(
            points, fill=GREEN, width=2, smooth=True
        )
    stock_chart_canvas.create_text(
        12, 8, anchor="nw", text=f"{stock.name} ({stock.symbol})",
        fill=WHITE, font=("Arial", 11, "bold")
    )
    stock_chart_canvas.create_text(
        width - 12, 8, anchor="ne", text=f"High {format_money(high)}",
        fill=GRAY, font=("Arial", 9)
    )
    stock_chart_canvas.create_text(
        12, height - 8, anchor="sw", text=f"Low {format_money(low)}",
        fill=GRAY, font=("Arial", 9)
    )


def refresh_stock_details():
    stock = selected_stock()
    holding = portfolio.holdings.get(
        stock.symbol, {"quantity": 0, "average_price": 0}
    )
    quantity = holding["quantity"]
    average_price = holding["average_price"]
    profit_loss = (stock.price - average_price) * quantity
    portfolio_value = sum(
        market_stock.price
        * portfolio.holdings.get(market_stock.symbol, {}).get("quantity", 0)
        for market_stock in stock_market.stocks.values()
    )
    if stock_price_label is not None:
        stock_price_label.config(text=f"{stock.symbol}  {format_money(stock.price)}")
    if stock_position_label is not None:
        stock_position_label.config(
            text=(
                f"High: {format_money(max(stock.history))}    "
                f"Low: {format_money(min(stock.history))}\n"
                f"Current price: {format_money(stock.price)}    "
                f"Profit: {format_money(profit_loss)}\n"
                f"Average bought price: {format_money(average_price)}    "
                f"Shares owned: {quantity}\n"
                f"Portfolio value: {format_money(portfolio_value)}"
            ),
            fg=GREEN if profit_loss >= 0 else RED
        )


def select_stock(symbol):
    global selected_stock_symbol
    selected_stock_symbol = symbol
    show_investing_mode("stocks", show_details=True)
    refresh_stock_chart()
    refresh_stock_details()


def change_stock_position(action):
    global balance
    try:
        quantity = int(stock_quantity_var.get())
    except (TypeError, ValueError):
        messagebox.showwarning("Invalid quantity", "Enter a whole number of shares.")
        return
    stock = selected_stock()
    portfolio.cash = balance
    if action == "buy":
        if not portfolio.buy(stock, quantity):
            messagebox.showwarning(
                "Not Enough Money",
                f"You need {format_money(stock.price * quantity)}."
            )
            return
        balance = portfolio.cash
        messagebox.showinfo(
            "Shares Purchased",
            f"Bought {quantity} share(s) of {stock.name}."
        )
    else:
        realized = portfolio.sell(stock, quantity)
        if realized is None:
            messagebox.showwarning(
                "Not Enough Shares", "You do not own that many shares."
            )
            return
        balance = portfolio.cash
        messagebox.showinfo(
            "Shares Sold",
            f"Realized P/L: {format_money(realized)}"
        )
    save_game_state()
    update_screen()
    refresh_stock_details()
    refresh_stock_rows()


def update_stock_market():
    stock_market.update()
    save_game_state()
    refresh_stock_chart()
    refresh_stock_details()
    refresh_stock_rows()
    root.after(5000, update_stock_market)


SHOP_CATEGORY_IMAGES = {
    "Cars": "Assets/Cars/Lamborghini_Huracan.jpg",
    "Jets": "Assets/Jets/Gulfstream_G700.jpg",
    "Yachts": "Assets/Yachts/Azimut_Grande.jpg",
}


def create_shop_category_tile(parent, category, image_path, command):
    with Image.open(image_path) as image:
        source_image = image.convert("RGB")
    tile = tk.Canvas(
        parent, bg=PANEL, highlightthickness=0, cursor="hand2"
    )
    photo = None

    def resize_tile(event):
        nonlocal photo
        width = max(event.width, 1)
        height = max(event.height, 1)
        image = ImageOps.fit(source_image, (width, height))
        image = ImageEnhance.Brightness(image).enhance(0.55)
        photo = ImageTk.PhotoImage(image)
        tile.delete("all")
        tile.create_image(0, 0, image=photo, anchor="nw")
        tile.create_text(
            width // 2, height // 2,
            text=category.upper(),
            fill=WHITE,
            font=("Arial", 30, "bold"),
        )

    tile.bind("<Configure>", resize_tile)

    def open_category(event):
        if event.widget is tile:
            command()

    tile.bind("<Button-1>", open_category)
    return tile


def show_shop_category(category=None):
    for widget in page_content.winfo_children():
        widget.destroy()

    if category is None:
        choices = tk.Frame(page_content, bg=BG)
        choices.pack(fill="both", expand=True)
        for shop_category, image_path in SHOP_CATEGORY_IMAGES.items():
            tile = create_shop_category_tile(
                choices,
                shop_category,
                image_path,
                lambda selected=shop_category: show_shop_category(selected),
            )
            tile.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        return

    category_header = tk.Frame(page_content, bg=BG)
    category_header.pack(fill="x", pady=(0, 8))
    make_button(
        category_header,
        text="< SHOP CATEGORIES",
        command=show_shop_category,
    ).pack(side="left", padx=(0, 12))
    tk.Label(
        category_header,
        text=category.upper(),
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=WHITE,
    ).pack(side="left")
    render_asset_list(page_content, [category], show_buy=True)


# =========================================================
# IMAGE LOADING
# =========================================================

image_cache = {}


def make_placeholder_image(label, bg_color="#26384a", accent_color="#00e676"):
    label_text = (label or "ASSET")[:12]
    image = Image.new("RGB", (180, 100), bg_color)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((8, 8, 172, 92), radius=12, fill=bg_color, outline=accent_color)
    draw.rectangle((18, 18, 162, 82), fill=(18, 32, 48))
    draw.text((22, 34), label_text.upper(), fill=accent_color, font=None)
    return image


def load_image(url, size=(180, 100)):
    if not url:
        url = "placeholder"
    cache_key = (url, size)
    if cache_key in image_cache:
        return image_cache[cache_key]

    try:
        if isinstance(url, str) and Path(url).exists():
            image = Image.open(url)
        else:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            if "image" not in response.headers.get("Content-Type", "").lower():
                raise ValueError("URL did not return an image")
            image = Image.open(BytesIO(response.content))

        image = image.convert("RGB")
        image.thumbnail(size)
        photo = ImageTk.PhotoImage(image)
        image_cache[cache_key] = photo
        return photo
    except Exception:
        image = make_placeholder_image(str(url).split("/")[-1].replace("%20", " ").replace(".jpg", "").replace(".png", ""))
        image = image.resize(size)
        photo = ImageTk.PhotoImage(image)
        image_cache[cache_key] = photo
        return photo


# =========================================================
# GAME LAYOUT AND PAGES
# =========================================================

left_panel = tk.Frame(root, bg=PANEL, width=250)
left_panel.pack(side="left", fill="y", padx=10, pady=10)

tk.Label(
    left_panel, text="💰 WEALTH\nCLICKER", font=("Arial", 24, "bold"),
    bg=PANEL, fg=WHITE
).pack(pady=30)

tk.Label(
    left_panel, text="BANK ACCOUNT", font=("Arial", 12),
    bg=PANEL, fg=GRAY
).pack()

balance_label = tk.Label(
    left_panel, text="$0", font=("Arial", 32, "bold"), bg=PANEL, fg=GREEN
)
balance_label.pack(pady=10)

income_label = tk.Label(
    left_panel, text="Passive income: $0/min", font=("Arial", 12),
    bg=PANEL, fg=GREEN
)
income_label.pack(pady=(0, 20))

page_area = tk.Frame(root, bg=BG)
page_area.pack(side="left", fill="both", expand=True, padx=10, pady=10)

navigation = tk.Frame(page_area, bg=BG)
navigation.pack(fill="x", pady=(0, 10))

page_content = tk.Frame(page_area, bg=BG)
page_content.pack(fill="both", expand=True)

current_page = "Home"


def bind_mousewheel(widget, scroll_target=None):
    if scroll_target is None:
        scroll_target = widget
    try:
        scroll_target.configure(yscrollincrement=1)
    except Exception:
        pass

    def _on_mousewheel(event):
        try:
            pixel_delta = -event.delta / 120 * 60
            pixel_delta += getattr(scroll_target, "_wheel_remainder", 0)
            pixel_step = int(pixel_delta)
            scroll_target._wheel_remainder = pixel_delta - pixel_step
            if pixel_step:
                scroll_target.yview_scroll(pixel_step, "units")
        except Exception:
            pass

    widget.bind("<MouseWheel>", _on_mousewheel)
    widget.bind("<Shift-MouseWheel>", _on_mousewheel)
    for child in widget.winfo_children():
        bind_mousewheel(child, scroll_target)
    return widget


def create_scrollable(parent, columns=1):
    canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    body = tk.Frame(canvas, bg=BG)
    body.bind("<Configure>", lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")
    ))
    window = canvas.create_window((0, 0), window=body, anchor="nw")
    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfigure(window, width=event.width)
    )
    canvas.configure(yscrollcommand=scrollbar.set)
    bind_mousewheel(canvas)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return body, canvas


def asset_card(parent, asset, show_buy=True, wide=False, upgrade_type=None):
    card = tk.Frame(parent, bg="#13263a", bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=8)
    if wide:
        card.configure(height=240)
        card.pack_propagate(False)

    photo = load_image(asset["image"], size=(360, 200) if wide else (180, 100))
    image_label = tk.Label(card, image=photo, bg="#13263a")
    image_label.image = photo
    image_label.pack(side="left", padx=8, pady=8)

    info = tk.Frame(card, bg="#13263a")
    info.pack(side="left", fill="both", expand=True)
    details = tk.Frame(info, bg="#13263a")
    details.pack(expand=True, anchor="w")
    tk.Label(
        details, text=asset["name"], font=("Arial", 14, "bold"),
        bg="#13263a", fg=WHITE
    ).pack(anchor="w", pady=(0, 5) if wide else (15, 5))

    upgrade_choice = None
    upgrade_buttons = {}
    final_price_text = tk.StringVar(master=card, value=f"${asset['price']:,.2f}")
    if upgrade_type:
        upgrade_choice = tk.StringVar(master=card, value="basic")
        tk.Label(
            details, text="ENGINE", font=("Arial", 9, "bold"),
            bg="#13263a", fg=GRAY
        )
        upgrade_label = "ENGINE" if upgrade_type == "engine" else "CREW"
        details.winfo_children()[-1].configure(text=upgrade_label)
        details.winfo_children()[-1].pack(anchor="w", pady=(10, 4))
        upgrade_options = tk.Frame(details, bg="#13263a")
        upgrade_options.pack(anchor="w")

        def select_upgrade(option):
            upgrade_choice.set(option)
            price = asset["price"] * (1.10 if option == "standard" else 1)
            final_price_text.set(f"${price:,.2f}")
            for button_option, button in upgrade_buttons.items():
                set_button_selected(
                    button,
                    button_option == option,
                    default_bg="#20384e",
                    default_fg=WHITE,
                    selected_bg=GREEN,
                    selected_fg="black",
                )

        for option, label in (
            ("basic", f"BASIC {upgrade_label}  +0%"),
            ("standard", f"STANDARD {upgrade_label}  +10%"),
        ):
            button = make_button(
                upgrade_options,
                text=label,
                command=lambda selected_option=option: select_upgrade(selected_option),
                selected=option == "basic",
                default_bg="#20384e",
                default_fg=WHITE,
                selected_bg=GREEN,
                selected_fg="black",
            )
            button.configure(font=("Arial", 10, "bold"), padx=9, pady=9)
            button.pack(side="left", padx=(0, 6))
            upgrade_buttons[option] = button

    price_parent = info
    if wide:
        price_parent = tk.Frame(card, bg="#13263a")
        price_parent.configure(width=190)
        price_parent.pack(side="right", fill="y", padx=16)
        price_parent.pack_propagate(False)

    if upgrade_type:
        tk.Label(
            price_parent, text="FINAL PRICE", font=("Arial", 9, "bold"),
            bg="#13263a", fg=GRAY
        ).pack(anchor="e", pady=(42, 2))

    tk.Label(
        price_parent,
        textvariable=final_price_text if upgrade_type else None,
        text="" if upgrade_type else f"${asset['price']:,}",
        font=("Arial", 20 if upgrade_type else 18, "bold"),
        bg="#13263a", fg=GREEN
    ).pack(anchor="e" if wide else "w", pady=(0, 8) if upgrade_type else 0)

    if "income_per_minute" in asset:
        tk.Label(
            details, text=f"+${asset['income_per_minute']:,.2f} per minute",
            font=("Arial", 11), bg="#13263a", fg="#8fffc4"
        ).pack(anchor="w", pady=(2, 0))

    if show_buy:
        is_owned = asset["name"] in owned
        buy_button = make_button(
            price_parent,
            text="OWNED" if is_owned else "BUY",
            command=lambda a=asset: buy_asset(
                a,
                purchase_price=(
                    round(a["price"] * (1.10 if upgrade_choice.get() == "standard" else 1), 2)
                    if upgrade_choice else None
                ),
                upgrade_option=(upgrade_choice.get().title() if upgrade_choice else None),
                upgrade_type=upgrade_type,
            ),
            default_bg="#456078" if is_owned else GREEN,
            default_fg=WHITE if is_owned else "black",
            selected_bg=GREEN,
            selected_fg="black",
        )
        if upgrade_type:
            buy_button.configure(font=("Arial", 14, "bold"), padx=24, pady=12)
        buy_button.pack(anchor="e" if wide else "w", pady=8)


def render_asset_list(parent, categories, show_buy=True):
    body, canvas = create_scrollable(parent)
    for category in categories:
        tk.Label(
            body, text=category, font=("Arial", 16, "bold"),
            bg=BG, fg=WHITE
        ).pack(anchor="w", padx=10, pady=(12, 2))
        category_assets = sorted(
            assets[category],
            key=lambda asset: (asset["price"], asset["name"].lower())
        )
        for asset in category_assets:
            if not show_buy and asset["name"] not in owned:
                continue
            asset_card(
                body, asset, show_buy,
                wide=category in {"Cars", "Jets", "Yachts"},
                upgrade_type=(
                    "engine" if category == "Cars" and show_buy
                    else "crew" if category in {"Jets", "Yachts"} and show_buy
                    else None
                ),
            )
    bind_mousewheel(body, canvas)


def build_stock_detail(parent):
    global stock_chart_canvas, stock_price_label
    global stock_position_label, stock_quantity_var

    detail = tk.Frame(parent, bg=PANEL)
    detail.pack(fill="both", expand=True, padx=5, pady=5)
    stock_chart_canvas = tk.Canvas(
        detail, height=190, bg="#081522", highlightthickness=0
    )
    bind_mousewheel(stock_chart_canvas)
    stock_chart_canvas.pack(fill="x", padx=8, pady=(8, 4))

    controls = tk.Frame(detail, bg=PANEL)
    controls.pack(fill="x", padx=8, pady=3)
    stock_price_label = tk.Label(
        controls, text="", font=("Arial", 13, "bold"), bg=PANEL, fg=GREEN
    )
    stock_price_label.pack(side="left")
    stock_quantity_var = tk.StringVar(value="1")
    tk.Entry(
        controls, textvariable=stock_quantity_var, width=5,
        bg="#13263a", fg=WHITE, insertbackground=WHITE
    ).pack(side="right", padx=3)
    make_button(
        controls,
        text="SELL",
        command=lambda: change_stock_position("sell"),
        default_bg=RED,
        default_fg=WHITE,
        selected_bg=RED,
        selected_fg=WHITE,
    ).pack(side="right", padx=3)
    make_button(
        controls,
        text="BUY",
        command=lambda: change_stock_position("buy"),
        default_bg=GREEN,
        default_fg="black",
        selected_bg=GREEN,
        selected_fg="black",
    ).pack(side="right", padx=3)

    stock_position_label = tk.Label(
        detail, text="", justify="left", anchor="w",
        font=("Arial", 10), bg=PANEL, fg=GRAY
    )
    stock_position_label.pack(fill="x", padx=8, pady=(2, 3))

    refresh_stock_details()
    refresh_stock_chart()


def build_stock_market(parent):
    global stock_list_body
    market = tk.Frame(parent, bg=PANEL)
    market.pack(fill="both", expand=True, padx=5, pady=5)

    stock_list = tk.Frame(market, bg="#13263a")
    stock_list.pack(fill="both", expand=True, padx=8, pady=8)
    header = tk.Label(
        stock_list,
        text="Select a stock below  |  Price        Owned   Avg purchase      P/L",
        anchor="w", bg="#13263a", fg=GRAY, font=("Arial", 9)
    )
    header.pack(fill="x", padx=5, pady=3)
    list_canvas = tk.Canvas(
        stock_list, bg="#13263a", highlightthickness=0
    )
    bind_mousewheel(list_canvas)
    list_scroll = tk.Scrollbar(
        stock_list, orient="vertical", command=list_canvas.yview
    )
    list_body = tk.Frame(list_canvas, bg="#13263a")
    list_body.bind(
        "<Configure>",
        lambda event: list_canvas.configure(
            scrollregion=list_canvas.bbox("all")
        )
    )
    list_canvas.create_window((0, 0), window=list_body, anchor="nw")
    list_canvas.configure(yscrollcommand=list_scroll.set)
    list_canvas.pack(side="left", fill="both", expand=True)
    list_scroll.pack(side="right", fill="y")

    stocks = sorted(
        stock_market.stocks.values(),
        key=lambda stock: (stock.price, stock.name.lower())
    )
    for stock in stocks:
        holding = portfolio.holdings.get(
            stock.symbol, {"quantity": 0, "average_price": 0}
        )
        profit_loss = (
            stock.price - holding["average_price"]
        ) * holding["quantity"]
        row = tk.Frame(list_body, bg="#13263a")
        row.pack(fill="x", padx=3, pady=1)
        make_button(
            row,
            text=stock.symbol,
            command=lambda symbol=stock.symbol: select_stock(symbol),
            default_bg="#1b3850",
            default_fg=WHITE,
            selected_bg=GREEN,
            selected_fg="black",
        ).pack(side="left", padx=(0, 4))
        row_price = tk.Label(
            row, text="", width=12, anchor="e", bg="#13263a", fg=WHITE
        )
        row_price.pack(side="left")
        row_position = tk.Label(
            row,
            text=f"{holding['quantity']:>5}  {format_money(holding['average_price']):>14}  {format_money(profit_loss):>12}",
            width=38, anchor="e", bg="#13263a",
            fg=GREEN if profit_loss >= 0 else RED
        )
        row_position.pack(side="left")
        row.stock = stock
        row.row_price = row_price
        row.row_position = row_position

    stock_list_body = list_body
    refresh_stock_rows()


def refresh_stock_rows():
    stock_list = stock_list_body
    if stock_list is None:
        return
    rows = [
        row for row in stock_list.winfo_children()
        if getattr(row, "stock", None) is not None
    ]
    rows.sort(
        key=lambda row: (row.stock.price, row.stock.name.lower())
    )
    for row in rows:
        stock = getattr(row, "stock", None)
        holding = portfolio.holdings.get(
            stock.symbol, {"quantity": 0, "average_price": 0}
        )
        profit_loss = (
            stock.price - holding["average_price"]
        ) * holding["quantity"]
        row.row_price.config(text=format_money(stock.price))
        row.row_position.config(
            text=(
                f"{holding['quantity']:>5}  "
                f"{format_money(holding['average_price']):>14}  "
                f"{format_money(profit_loss):>12}"
            ),
            fg=GREEN if profit_loss >= 0 else RED
        )
    for row in rows:
        row.pack_forget()
        row.pack(fill="x", padx=3, pady=1)


def show_investing_mode(mode, show_details=False):
    global active_investing_mode
    active_investing_mode = mode
    if home_earning_frame is None or home_investing_content is None:
        return
    for widget in home_earning_frame.winfo_children():
        widget.destroy()
    for widget in home_investing_content.winfo_children():
        widget.destroy()

    if mode == "stocks":
        build_stock_market(home_investing_content)
        if show_details:
            build_stock_detail(home_earning_frame)
        else:
            tk.Label(
                home_earning_frame, text="Select a stock to view its chart",
                font=("Arial", 14), bg=PANEL, fg=GRAY
            ).pack(expand=True)
    else:
        tk.Label(
            home_earning_frame, text="EARNING", font=("Arial", 20, "bold"),
            bg=PANEL, fg=WHITE
        ).pack(pady=24)
        global money_button
        money_button = make_button(
            home_earning_frame,
            text="$",
            command=earn_money,
            default_bg="#063d27",
            default_fg=GREEN,
            selected_bg="#063d27",
            selected_fg=GREEN,
        )
        money_button.config(font=("Arial", 55, "bold"), width=5, height=2)
        money_button.pack(pady=45)
        tk.Label(
            home_earning_frame, text="CLICK TO EARN $1",
            font=("Arial", 16, "bold"), bg=PANEL, fg=GREEN
        ).pack()
        render_asset_list(home_investing_content, ["Real Estate"], show_buy=True)

    for key, button in home_investing_buttons.items():
        set_button_selected(
            button,
            key == mode,
            default_bg="#13263a",
            default_fg=WHITE,
            selected_bg=GREEN,
            selected_fg="black",
        )


def show_page(page):
    global current_page, money_button
    global home_earning_frame, home_investing_frame, home_investing_content
    global stock_chart_canvas, stock_price_label, stock_position_label
    global stock_list_body
    current_page = page
    stock_chart_canvas = None
    stock_list_body = None
    stock_price_label = None
    stock_position_label = None
    for widget in page_content.winfo_children():
        widget.destroy()

    if page == "Home":
        home = tk.Frame(page_content, bg=BG)
        home.pack(fill="both", expand=True)
        home_earning_frame = tk.Frame(home, bg=PANEL)
        home_earning_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        home_investing_frame = tk.Frame(home, bg=PANEL)
        home_investing_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        tk.Label(
            home_investing_frame, text="INVESTING", font=("Arial", 19, "bold"),
            bg=PANEL, fg=WHITE
        ).pack(pady=(8, 3))
        investing_tabs = tk.Frame(home_investing_frame, bg=PANEL)
        investing_tabs.pack(fill="x", padx=8, pady=(0, 5))
        home_investing_content = tk.Frame(home_investing_frame, bg=PANEL)
        home_investing_content.pack(fill="both", expand=True)
        home_investing_buttons.clear()
        home_investing_buttons["real_estate"] = make_button(
            investing_tabs,
            text="REAL ESTATE",
            command=lambda: show_investing_mode("real_estate"),
            selected=True,
            default_bg=GREEN,
            default_fg="black",
            selected_bg=GREEN,
            selected_fg="black",
        )
        home_investing_buttons["real_estate"].pack(side="left", fill="x", expand=True, padx=(0, 3))
        home_investing_buttons["stocks"] = make_button(
            investing_tabs,
            text="STOCK MARKET",
            command=lambda: show_investing_mode("stocks"),
            default_bg="#13263a",
            default_fg=WHITE,
            selected_bg=GREEN,
            selected_fg="black",
        )
        home_investing_buttons["stocks"].pack(side="left", fill="x", expand=True, padx=(3, 0))
        show_investing_mode("real_estate")

    elif page == "Businesses":
        businesses = tk.Frame(page_content, bg=BG)
        businesses.pack(fill="both", expand=True)
        owned_frame = tk.Frame(businesses, bg=PANEL)
        owned_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        all_frame = tk.Frame(businesses, bg=PANEL)
        all_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        tk.Label(
            owned_frame, text="MY COMPANIES", font=("Arial", 22, "bold"),
            bg=PANEL, fg=WHITE
        ).pack(pady=15)
        render_asset_list(owned_frame, ["Businesses"], show_buy=False)
        tk.Label(
            all_frame, text="ALL COMPANIES", font=("Arial", 22, "bold"),
            bg=PANEL, fg=WHITE
        ).pack(pady=15)
        render_asset_list(all_frame, ["Businesses"], show_buy=True)

    elif page == "Liabilities":
        tk.Label(
            page_content, text="MY LIABILITIES", font=("Arial", 26, "bold"),
            bg=BG, fg=WHITE
        ).pack(pady=(5, 15))
        render_asset_list(page_content, ["Cars", "Jets", "Yachts"], show_buy=False)

    elif page == "Shop":
        show_shop_category()

    for nav_page, button in navigation_buttons.items():
        set_button_selected(
            button,
            nav_page == current_page,
            default_bg="#13263a",
            default_fg=WHITE,
            selected_bg=GREEN,
            selected_fg="black",
        )


for page in ["Home", "Businesses", "Liabilities", "Shop"]:
    button = make_button(
        navigation,
        text=page,
        command=lambda p=page: show_page(p),
        default_bg="#13263a",
        default_fg=WHITE,
        selected_bg=GREEN,
        selected_fg="black",
    )
    navigation_buttons[page] = button
    button.pack(side="left", fill="x", expand=True, padx=2)


for page_name, button in navigation_buttons.items():
    set_button_selected(button, current_page == page_name, default_bg="#13263a", default_fg=WHITE,
                        selected_bg=GREEN, selected_fg="black")

show_page("Home")


# =========================================================
# START GAME
# =========================================================

def close_game():
    save_game_state()
    root.destroy()


update_screen()
root.after(1000, collect_passive_income)
root.after(5000, update_stock_market)
root.protocol("WM_DELETE_WINDOW", close_game)

root.mainloop()