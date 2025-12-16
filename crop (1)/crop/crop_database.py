"""
Extended Crop Database with 300+ crop varieties organized by category
"""

CROP_CATEGORIES = {
    'Cereals & Grains': [
        'Rice', 'Wheat', 'Maize', 'Barley', 'Oats', 'Rye', 'Millet', 'Sorghum', 
        'Quinoa', 'Buckwheat', 'Amaranth', 'Teff', 'Spelt', 'Triticale', 'Fonio',
        'Wild Rice', 'Kamut', 'Einkorn', 'Emmer', 'Job\'s Tears'
    ],
    'Pulses & Legumes': [
        'Chickpea', 'Lentil', 'Black Gram', 'Green Gram', 'Pigeon Pea', 'Kidney Beans',
        'Navy Beans', 'Pinto Beans', 'Black Beans', 'Lima Beans', 'Fava Beans',
        'Adzuki Beans', 'Mung Beans', 'Cowpea', 'Lupin', 'Soybean', 'Peanut',
        'Horse Gram', 'Moth Beans', 'Cluster Beans', 'Winged Beans', 'Velvet Beans',
        'Sword Beans', 'Jack Beans', 'Lablab Beans'
    ],
    'Vegetables - Leafy': [
        'Spinach', 'Lettuce', 'Cabbage', 'Kale', 'Swiss Chard', 'Collard Greens',
        'Mustard Greens', 'Arugula', 'Bok Choy', 'Chinese Cabbage', 'Endive',
        'Radicchio', 'Watercress', 'Mizuna', 'Tatsoi', 'Amaranth Greens',
        'Moringa Leaves', 'Drumstick Leaves', 'Fenugreek Leaves', 'Coriander',
        'Parsley', 'Celery', 'Fennel', 'Dill', 'Chervil'
    ],
    'Vegetables - Root': [
        'Potato', 'Carrot', 'Radish', 'Beet', 'Turnip', 'Sweet Potato', 'Yam',
        'Cassava', 'Taro', 'Ginger', 'Turmeric', 'Onion', 'Garlic', 'Shallot',
        'Leek', 'Parsnip', 'Rutabaga', 'Kohlrabi', 'Celeriac', 'Jerusalem Artichoke',
        'Lotus Root', 'Water Chestnut', 'Jicama', 'Daikon', 'Horseradish'
    ],
    'Vegetables - Fruit': [
        'Tomato', 'Eggplant', 'Bell Pepper', 'Chilli', 'Cucumber', 'Zucchini',
        'Pumpkin', 'Squash', 'Bottle Gourd', 'Bitter Gourd', 'Ridge Gourd',
        'Snake Gourd', 'Ash Gourd', 'Pointed Gourd', 'Ivy Gourd', 'Okra',
        'Drumstick', 'Brinjal', 'Green Beans', 'French Beans', 'Cluster Beans',
        'Snow Peas', 'Sugar Snap Peas', 'Corn', 'Baby Corn'
    ],
    'Vegetables - Cruciferous': [
        'Broccoli', 'Cauliflower', 'Brussels Sprouts', 'Romanesco', 'Kohlrabi',
        'Chinese Broccoli', 'Broccolini', 'Purple Cauliflower', 'Green Cauliflower'
    ],
    'Fruits - Tropical': [
        'Mango', 'Banana', 'Papaya', 'Pineapple', 'Coconut', 'Jackfruit',
        'Guava', 'Passion Fruit', 'Dragon Fruit', 'Lychee', 'Rambutan', 'Longan',
        'Durian', 'Mangosteen', 'Starfruit', 'Sapota', 'Custard Apple', 'Soursop',
        'Breadfruit', 'Tamarind', 'Pomelo', 'Avocado', 'Cherimoya', 'Acai',
        'Acerola', 'Jabuticaba', 'Camu Camu', 'Cupuacu'
    ],
    'Fruits - Citrus': [
        'Orange', 'Lemon', 'Lime', 'Grapefruit', 'Tangerine', 'Mandarin',
        'Clementine', 'Kumquat', 'Bergamot', 'Citron', 'Yuzu', 'Finger Lime',
        'Blood Orange', 'Cara Cara Orange', 'Meyer Lemon', 'Key Lime'
    ],
    'Fruits - Temperate': [
        'Apple', 'Pear', 'Peach', 'Plum', 'Cherry', 'Apricot', 'Nectarine',
        'Quince', 'Persimmon', 'Fig', 'Pomegranate', 'Kiwi', 'Grape',
        'Mulberry', 'Loquat', 'Medlar', 'Jujube', 'Gooseberry', 'Currant'
    ],
    'Fruits - Berries': [
        'Strawberry', 'Blueberry', 'Raspberry', 'Blackberry', 'Cranberry',
        'Elderberry', 'Goji Berry', 'Acai Berry', 'Boysenberry', 'Loganberry',
        'Marionberry', 'Cloudberry', 'Lingonberry', 'Salmonberry', 'Huckleberry'
    ],
    'Fruits - Melons': [
        'Watermelon', 'Muskmelon', 'Cantaloupe', 'Honeydew', 'Casaba Melon',
        'Persian Melon', 'Galia Melon', 'Crenshaw Melon', 'Santa Claus Melon',
        'Winter Melon', 'Sprite Melon', 'Korean Melon'
    ],
    'Oilseeds': [
        'Sunflower', 'Groundnut', 'Mustard', 'Sesame', 'Safflower', 'Linseed',
        'Rapeseed', 'Niger Seed', 'Castor', 'Palm', 'Olive', 'Coconut Oil Palm',
        'Soybean', 'Cotton Seed', 'Hemp Seed', 'Chia', 'Perilla', 'Camelina'
    ],
    'Fiber Crops': [
        'Cotton', 'Jute', 'Hemp', 'Flax', 'Kenaf', 'Ramie', 'Sisal', 'Coir',
        'Abaca', 'Sunn Hemp', 'Roselle', 'Mesta'
    ],
    'Spices': [
        'Black Pepper', 'Cardamom', 'Cinnamon', 'Clove', 'Nutmeg', 'Mace',
        'Turmeric', 'Ginger', 'Cumin', 'Coriander Seeds', 'Fennel Seeds',
        'Fenugreek Seeds', 'Mustard Seeds', 'Anise', 'Star Anise', 'Vanilla',
        'Saffron', 'Curry Leaf', 'Bay Leaf', 'Allspice', 'Paprika', 'Cayenne',
        'White Pepper', 'Long Pepper', 'Grains of Paradise'
    ],
    'Herbs': [
        'Basil', 'Mint', 'Oregano', 'Thyme', 'Rosemary', 'Sage', 'Marjoram',
        'Tarragon', 'Chives', 'Lemongrass', 'Lavender', 'Chamomile', 'Stevia',
        'Tulsi', 'Ashwagandha', 'Brahmi', 'Neem', 'Aloe Vera', 'Giloy'
    ],
    'Beverage Crops': [
        'Tea', 'Coffee', 'Cocoa', 'Yerba Mate', 'Guarana', 'Kola Nut'
    ],
    'Sugar Crops': [
        'Sugarcane', 'Sugar Beet', 'Sweet Sorghum', 'Stevia', 'Date Palm',
        'Palm Sugar', 'Maple'
    ],
    'Fodder Crops': [
        'Alfalfa', 'Clover', 'Ryegrass', 'Timothy', 'Bermuda Grass', 'Sudan Grass',
        'Napier Grass', 'Berseem', 'Lucerne', 'Oat Fodder', 'Maize Fodder',
        'Sorghum Fodder', 'Cowpea Fodder', 'Guar Fodder'
    ],
    'Medicinal Crops': [
        'Aloe Vera', 'Tulsi', 'Ashwagandha', 'Brahmi', 'Neem', 'Giloy',
        'Shatavari', 'Amla', 'Haritaki', 'Bibhitaki', 'Guduchi', 'Kalmegh',
        'Isabgol', 'Senna', 'Safed Musli', 'Pippali', 'Chitrak', 'Punarnava'
    ],
    'Flowers': [
        'Rose', 'Marigold', 'Jasmine', 'Chrysanthemum', 'Tuberose', 'Gladiolus',
        'Carnation', 'Gerbera', 'Orchid', 'Anthurium', 'Lily', 'Dahlia',
        'Sunflower Ornamental', 'Zinnia', 'Aster', 'Petunia', 'Hibiscus'
    ],
    'Nuts': [
        'Almond', 'Cashew', 'Walnut', 'Pistachio', 'Hazelnut', 'Macadamia',
        'Brazil Nut', 'Pine Nut', 'Pecan', 'Chestnut', 'Betel Nut', 'Areca Nut'
    ]
}

EXTENDED_CROPS = []
for category, crops in CROP_CATEGORIES.items():
    EXTENDED_CROPS.extend(crops)

EXTENDED_CROPS = list(set(EXTENDED_CROPS))
EXTENDED_CROPS.sort()

SOIL_TYPES = ['Clay', 'Loam', 'Sandy', 'Silt', 'Clay Loam', 'Sandy Loam', 'Red', 'Black', 'Alluvial', 'Laterite', 'Peaty', 'Saline']
SEASONS = ['Kharif (Monsoon)', 'Rabi (Winter)', 'Zaid (Summer)', 'Perennial']
CROP_DURATIONS = ['Short-term (< 4 months)', 'Medium-term (4-8 months)', 'Long-term (> 8 months)', 'Perennial']

GROWTH_STAGES = ['Germination', 'Seedling', 'Vegetative', 'Flowering', 'Fruiting/Grain Filling', 'Maturity', 'Harvest']

EXTENDED_MULTI_CROP_COMBINATIONS = {
    'Rice': {
        'companions': ['Azolla (green manure)', 'Fish (Integrated farming)', 'Duck (Integrated farming)', 'Shrimp'],
        'spacing_main': '20x15 cm',
        'spacing_companion': 'Continuous cover / 1 fish per 2 sq.m',
        'benefits': 'Nitrogen fixation, additional protein source, pest control, weed management',
        'irrigation': 'Maintain 5-7 cm water depth, drain before harvest',
        'yield_boost': '15-25%',
        'color': '#4CAF50',
        'icon': '🌾'
    },
    'Maize': {
        'companions': ['Beans', 'Pumpkin', 'Squash', 'Cowpea', 'Sunflower'],
        'spacing_main': '60x25 cm',
        'spacing_companion': 'Beans: between rows, Pumpkin: 2m apart at field edges',
        'benefits': 'Three Sisters method - nitrogen fixation, ground cover, vertical space use',
        'irrigation': 'Drip irrigation every 3-4 days, 2-3 L per plant',
        'yield_boost': '20-30%',
        'color': '#FFC107',
        'icon': '🌽'
    },
    'Sugarcane': {
        'companions': ['Onion', 'Garlic', 'Coriander', 'Potato', 'Turmeric', 'Ginger'],
        'spacing_main': '90x45 cm',
        'spacing_companion': 'Inter-row planting at 15cm spacing',
        'benefits': 'Early income, weed suppression, efficient land use',
        'irrigation': 'Furrow irrigation weekly, companions benefit from residual moisture',
        'yield_boost': '10-20%',
        'color': '#8BC34A',
        'icon': '🎋'
    },
    'Cotton': {
        'companions': ['Groundnut', 'Soybean', 'Black gram', 'Green gram', 'Cowpea'],
        'spacing_main': '90x60 cm',
        'spacing_companion': '30x10 cm between cotton rows',
        'benefits': 'Nitrogen fixation, soil health, additional oil/pulse income',
        'irrigation': 'Alternate row irrigation, 5-7 day interval',
        'yield_boost': '15-25%',
        'color': '#E3F2FD',
        'icon': '☁️'
    },
    'Tomato': {
        'companions': ['Basil', 'Marigold', 'Carrot', 'Onion', 'Parsley', 'Chives'],
        'spacing_main': '60x45 cm',
        'spacing_companion': 'Basil: 30cm from tomato, Marigold: border planting',
        'benefits': 'Pest repellent, pollinator attraction, flavor enhancement',
        'irrigation': 'Drip irrigation daily, 1.5-2 L per plant',
        'yield_boost': '20-35%',
        'color': '#F44336',
        'icon': '🍅'
    },
    'Wheat': {
        'companions': ['Mustard', 'Chickpea', 'Lentil', 'Peas', 'Berseem'],
        'spacing_main': '22.5 cm row spacing',
        'spacing_companion': 'Every 4th row or border planting',
        'benefits': 'Additional oilseed/pulse crop, biodiversity, risk distribution',
        'irrigation': 'Flood irrigation at critical stages (CRI, jointing, flowering)',
        'yield_boost': '10-20%',
        'color': '#FFD54F',
        'icon': '🌾'
    },
    'Potato': {
        'companions': ['Beans', 'Cabbage', 'Marigold', 'Horseradish', 'Corn'],
        'spacing_main': '60x20 cm',
        'spacing_companion': 'Beans in alternate rows, Marigold as border',
        'benefits': 'Pest deterrent, space optimization, soil nitrogen',
        'irrigation': 'Ridge irrigation every 7-10 days, avoid waterlogging',
        'yield_boost': '15-25%',
        'color': '#795548',
        'icon': '🥔'
    },
    'Groundnut': {
        'companions': ['Sunflower', 'Maize', 'Sorghum', 'Castor', 'Pearl Millet'],
        'spacing_main': '30x10 cm',
        'spacing_companion': 'Tall crops at 2:6 or 2:8 row ratio',
        'benefits': 'Windbreak, additional oilseed income, erosion control',
        'irrigation': 'Sprinkler or drip, maintain soil moisture 50-60%',
        'yield_boost': '15-20%',
        'color': '#8D6E63',
        'icon': '🥜'
    },
    'Onion': {
        'companions': ['Carrot', 'Lettuce', 'Beet', 'Tomato', 'Strawberry'],
        'spacing_main': '15x10 cm',
        'spacing_companion': 'Alternating beds or rows',
        'benefits': 'Pest confusion, efficient space use, harvest timing diversity',
        'irrigation': 'Light frequent irrigation, drip preferred',
        'yield_boost': '20-30%',
        'color': '#9C27B0',
        'icon': '🧅'
    },
    'Cabbage': {
        'companions': ['Celery', 'Onion', 'Dill', 'Chamomile', 'Rosemary'],
        'spacing_main': '45x45 cm',
        'spacing_companion': 'Border and inter-row planting',
        'benefits': 'Pest repellent, beneficial insect attraction',
        'irrigation': 'Consistent moisture, drip or sprinkler every 2-3 days',
        'yield_boost': '15-25%',
        'color': '#4DB6AC',
        'icon': '🥬'
    },
    'Mango': {
        'companions': ['Turmeric', 'Ginger', 'Papaya', 'Banana', 'Pineapple'],
        'spacing_main': '10x10 m',
        'spacing_companion': 'Between mango trees during initial years',
        'benefits': 'Land use efficiency, early income, shade tolerance',
        'irrigation': 'Basin irrigation, monthly during dry season',
        'yield_boost': '25-40%',
        'color': '#FF9800',
        'icon': '🥭'
    },
    'Banana': {
        'companions': ['Elephant Foot Yam', 'Turmeric', 'Ginger', 'Pineapple', 'Papaya'],
        'spacing_main': '2x2 m or 2.5x2.5 m',
        'spacing_companion': 'Between banana plants',
        'benefits': 'Efficient space use, additional income, soil cover',
        'irrigation': 'Drip irrigation, 10-15 L per plant daily',
        'yield_boost': '30-45%',
        'color': '#FFEB3B',
        'icon': '🍌'
    },
    'Coffee': {
        'companions': ['Pepper', 'Cardamom', 'Orange', 'Vanilla', 'Cocoa'],
        'spacing_main': '2.5x2.5 m',
        'spacing_companion': 'As shade or intercrops',
        'benefits': 'Shade provision, additional high-value crops, biodiversity',
        'irrigation': 'Sprinkler or drip, 30-40 mm/week',
        'yield_boost': '20-35%',
        'color': '#5D4037',
        'icon': '☕'
    },
    'Coconut': {
        'companions': ['Cocoa', 'Pepper', 'Pineapple', 'Banana', 'Turmeric'],
        'spacing_main': '7.5x7.5 m',
        'spacing_companion': 'In coconut basins and interspaces',
        'benefits': 'Multi-tier cropping, year-round income, land optimization',
        'irrigation': 'Basin or drip irrigation',
        'yield_boost': '40-60%',
        'color': '#4E342E',
        'icon': '🥥'
    },
    'Chilli': {
        'companions': ['Onion', 'Garlic', 'Marigold', 'Coriander', 'Fenugreek'],
        'spacing_main': '60x45 cm',
        'spacing_companion': 'Border and intercrop planting',
        'benefits': 'Pest management, companion effects, soil health',
        'irrigation': 'Drip irrigation, 2-3 L per plant',
        'yield_boost': '15-25%',
        'color': '#D32F2F',
        'icon': '🌶️'
    },
    'Cucumber': {
        'companions': ['Sunflower', 'Beans', 'Peas', 'Radish', 'Lettuce'],
        'spacing_main': '120x60 cm',
        'spacing_companion': 'Sunflower as border, others intercropped',
        'benefits': 'Pollinator attraction, nitrogen fixation, quick harvest',
        'irrigation': 'Drip irrigation daily, 2-3 L per plant',
        'yield_boost': '20-30%',
        'color': '#8BC34A',
        'icon': '🥒'
    },
    'Watermelon': {
        'companions': ['Corn', 'Sunflower', 'Radish', 'Beans'],
        'spacing_main': '3x2 m',
        'spacing_companion': 'Border planting, radish as trap crop',
        'benefits': 'Windbreak, pest management, early harvest intercrop',
        'irrigation': 'Furrow or drip, 5-8 L per plant',
        'yield_boost': '15-25%',
        'color': '#E91E63',
        'icon': '🍉'
    },
    'Apple': {
        'companions': ['Peas', 'Beans', 'Clover', 'Nasturtium', 'Chives'],
        'spacing_main': '5x5 m',
        'spacing_companion': 'Ground cover and border planting',
        'benefits': 'Nitrogen fixation, pollinator attraction, pest control',
        'irrigation': 'Drip or micro-sprinkler, 30-50 L per tree',
        'yield_boost': '10-20%',
        'color': '#C62828',
        'icon': '🍎'
    },
    'Grapes': {
        'companions': ['Roses', 'Garlic', 'Chives', 'Oregano', 'Beans'],
        'spacing_main': '3x2 m',
        'spacing_companion': 'End of rows and interrows',
        'benefits': 'Disease indicators, pest repellent, nitrogen fixation',
        'irrigation': 'Drip irrigation, 4-6 L per vine daily',
        'yield_boost': '15-20%',
        'color': '#7B1FA2',
        'icon': '🍇'
    },
    'Soybean': {
        'companions': ['Maize', 'Sorghum', 'Sunflower', 'Castor'],
        'spacing_main': '45x5 cm',
        'spacing_companion': 'Tall crops at 4:2 row ratio',
        'benefits': 'Nitrogen fixation, windbreak, diversification',
        'irrigation': 'Sprinkler or flood, 40-50 mm/week',
        'yield_boost': '15-25%',
        'color': '#8BC34A',
        'icon': '🫘'
    }
}

CROP_ICONS = {
    'Rice': '🌾', 'Wheat': '🌾', 'Maize': '🌽', 'Cotton': '☁️', 'Sugarcane': '🎋',
    'Groundnut': '🥜', 'Soybean': '🫘', 'Sunflower': '🌻', 'Tomato': '🍅', 'Potato': '🥔',
    'Onion': '🧅', 'Chilli': '🌶️', 'Cabbage': '🥬', 'Cauliflower': '🥦', 'Carrot': '🥕',
    'Beans': '🫛', 'Peas': '🟢', 'Cucumber': '🥒', 'Watermelon': '🍉', 'Mango': '🥭',
    'Banana': '🍌', 'Apple': '🍎', 'Orange': '🍊', 'Grapes': '🍇', 'Papaya': '🍈',
    'Coconut': '🥥', 'Coffee': '☕', 'Tea': '🍵', 'Pomegranate': '🍎', 'Lemon': '🍋',
    'Strawberry': '🍓', 'Cherry': '🍒', 'Peach': '🍑', 'Pear': '🍐', 'Pineapple': '🍍',
    'Kiwi': '🥝', 'Avocado': '🥑', 'Broccoli': '🥦', 'Lettuce': '🥬', 'Corn': '🌽',
    'Mushroom': '🍄', 'Garlic': '🧄', 'Ginger': '🫚', 'Bell Pepper': '🫑', 'Eggplant': '🍆',
    'Sweet Potato': '🍠', 'Olive': '🫒', 'Cocoa': '🍫', 'Vanilla': '🌼', 'Cinnamon': '🌿',
    'Black Pepper': '⚫', 'Cardamom': '💚', 'Turmeric': '🟡', 'Rose': '🌹', 'Jasmine': '🌸',
    'Marigold': '🌼', 'Orchid': '🪻', 'Lily': '🌷', 'Hibiscus': '🌺', 'Lavender': '💜'
}

def get_crop_icon(crop_name):
    return CROP_ICONS.get(crop_name, '🌱')

def get_crop_category(crop_name):
    for category, crops in CROP_CATEGORIES.items():
        if crop_name in crops:
            return category
    return 'Other'

CROP_INFO = {
    'Rice': {'season': 'Kharif', 'duration': '120-150 days', 'water': 'High', 'soil': 'Clay, Loam'},
    'Wheat': {'season': 'Rabi', 'duration': '120-140 days', 'water': 'Medium', 'soil': 'Loam, Clay Loam'},
    'Maize': {'season': 'Kharif/Rabi', 'duration': '90-120 days', 'water': 'Medium', 'soil': 'Well-drained loam'},
    'Cotton': {'season': 'Kharif', 'duration': '150-180 days', 'water': 'Medium', 'soil': 'Black, Clay'},
    'Sugarcane': {'season': 'Kharif', 'duration': '12-18 months', 'water': 'High', 'soil': 'Loam, Clay Loam'},
    'Tomato': {'season': 'All', 'duration': '90-120 days', 'water': 'Medium', 'soil': 'Well-drained loam'},
    'Potato': {'season': 'Rabi', 'duration': '90-120 days', 'water': 'Medium', 'soil': 'Sandy Loam'},
    'Onion': {'season': 'Rabi', 'duration': '90-150 days', 'water': 'Low-Medium', 'soil': 'Loam'},
    'Mango': {'season': 'Perennial', 'duration': '3-6 years to fruit', 'water': 'Medium', 'soil': 'Well-drained'},
    'Banana': {'season': 'All', 'duration': '10-12 months', 'water': 'High', 'soil': 'Rich loam'},
}

print(f"Total crops in database: {len(EXTENDED_CROPS)}")
