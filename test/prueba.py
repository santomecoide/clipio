from semantics import SemanticIndex

text1 = "Muy alejados luz, más allá alejados de las montañas los ñeros de palabras, alejados de los países lejos de las vocales y las consonantes, viven los textos simulados. viven aislados en casas de letras, en la costa de la semántica, un gran océano de lenguas. Un riachuelo llamado Pons fluye por su pueblo y los abastece con las normas necesarias."
text2 = "Hablamos de un país paraisomático en el que a uno le caen pedazos de frases asadas en la boca."
text3 = "Ni siquiera los todopoderosos signos de puntuación dominan a los textos simulados; una vida, se puede decir, poco ortográfica"

si = SemanticIndex()
si.add_document("uuid1", text1)
#si.add_document("uuid2", text2)
#si.add_document("uuid3", text3)