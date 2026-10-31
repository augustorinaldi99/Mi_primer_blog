perfil_autor = {
    "nombre": "Augusto Rinaldi",
    "bio": "Crítico de películas",
    "especialidad": "Universo de superhéroes",
    "redes_sociales": [
        "@augustorinaldi",
        "@augustorinaldi_movies",
        "@augustorinaldi_moives.ok"
    ]
}

estados_post = ("borrador", "archivado", "publicado")


posts = [
    {
        "id": 1,
        "titulo": "Qué es el MCU",
        "contenido": "Explicación del Universo Cinematográfico de Marvel.",
        "autor": perfil_autor,
        "tags": ["#Marvel", "#Avengers", "#MCU"],
        "estado": "publicado"
    },
    {
        "id": 2,
        "titulo": "Explicación del Multiverso",
        "contenido": "Una explicación de distintas realidades y líneas temporales.",
        "autor": perfil_autor,
        "tags": ["#Multiverso", "#Timeline", "#Spiderverse"],
        "estado": "borrador"
    },
    {
        "id": 3,
        "titulo": "Top 10 personajes más poderosos",
        "contenido": "Un listado de personajes poderosos del universo Marvel.",
        "autor": perfil_autor,
        "tags": ["#Spiderman", "#Thor", "#DoctorDoom", "#Wanda", "#Thanos", "#CapitanaMarvel"],
        "estado": "archivado"
    },
    {
        "id": 4,
        "titulo": "Post incompleto para probar la validación",
        "autor": perfil_autor,
        "tags": ["#Testeo"],
        "estado": "borrador"
    }
]

etiquetas_blog = {
                    "#Marvel", "#MCU", "#Avengers", "#Multiverso",
                    "#Timeline", "#X-men", "#Thedefenders"
}
etiquetas_blog = set(etiquetas_blog)