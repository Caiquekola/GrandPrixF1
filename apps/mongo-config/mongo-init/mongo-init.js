db = db.getSiblingDB("base_gp");

db.cars.insertMany([
  // Flamengo
  { "_id": "01", "car_number": 1,  "country": "BRA", "driver": "Zico",              "team": "Flamengo" },
  { "_id": "02", "car_number": 2,  "country": "BRA", "driver": "Adriano Imperador", "team": "Flamengo" },

  // Palmeiras
  { "_id": "03", "car_number": 3,  "country": "BRA", "driver": "Ademir da Guia",    "team": "Palmeiras" },
  { "_id": "04", "car_number": 4,  "country": "BRA", "driver": "Marcos",            "team": "Palmeiras" },

  // São Paulo
  { "_id": "05", "car_number": 5,  "country": "BRA", "driver": "Rogério Ceni",      "team": "São Paulo" },
  { "_id": "06", "car_number": 6,  "country": "BRA", "driver": "Raí",               "team": "São Paulo" },

  // Corinthians
  { "_id": "07", "car_number": 7,  "country": "BRA", "driver": "Sócrates",          "team": "Corinthians" },
  { "_id": "08", "car_number": 8,  "country": "BRA", "driver": "Marcelinho Carioca","team": "Corinthians" },

  // Atlético Mineiro
  { "_id": "09", "car_number": 9,  "country": "BRA", "driver": "Reinaldo",          "team": "Atlético Mineiro" },
  { "_id": "10", "car_number": 10, "country": "BRA", "driver": "Ronaldinho Gaúcho", "team": "Atlético Mineiro" },

  // Grêmio
  { "_id": "11", "car_number": 11, "country": "BRA", "driver": "Renato Gaúcho",     "team": "Grêmio" },
  { "_id": "12", "car_number": 12, "country": "BRA", "driver": "Kannemann",         "team": "Grêmio" },

  // Internacional
  { "_id": "13", "car_number": 13, "country": "BRA", "driver": "Falcão",            "team": "Internacional" },
  { "_id": "14", "car_number": 14, "country": "BRA", "driver": "Fernandão",         "team": "Internacional" },

  // Santos
  { "_id": "15", "car_number": 15, "country": "BRA", "driver": "Pelé",              "team": "Santos" },
  { "_id": "16", "car_number": 16, "country": "BRA", "driver": "Neymar",            "team": "Santos" },

  // Fluminense
  { "_id": "17", "car_number": 17, "country": "BRA", "driver": "Fred",              "team": "Fluminense" },
  { "_id": "18", "car_number": 18, "country": "BRA", "driver": "Rivellino",         "team": "Fluminense" },

  // Botafogo
  { "_id": "19", "car_number": 19, "country": "BRA", "driver": "Garrincha",         "team": "Botafogo" },
  { "_id": "20", "car_number": 20, "country": "BRA", "driver": "Nilton Santos",     "team": "Botafogo" },

  // Vasco
  { "_id": "21", "car_number": 21, "country": "BRA", "driver": "Roberto Dinamite",  "team": "Vasco" },
  { "_id": "22", "car_number": 22, "country": "BRA", "driver": "Romário",           "team": "Vasco" },

  // Cruzeiro
  { "_id": "23", "car_number": 23, "country": "BRA", "driver": "Tostão",            "team": "Cruzeiro" },
  { "_id": "24", "car_number": 24, "country": "BRA", "driver": "Alex",              "team": "Cruzeiro" }
]);

