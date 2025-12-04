Model Markowa w analizie języka
zamówień publicznych
2025
Cel
Projekt ma na celu zastosowanie metod analizy języka naturalnego i
prostych modeli uczenia maszynowego w analizie opisów zamówień
publicznych. Należy opracować model Markowa – który zostanie użyty do
badania sekwencyjnych wzorców językowych. Projekt łączy elementy Big
Data z NLP oraz interpretowalnej sztucznej inteligencji (explainable AI).
Zbiór danych
Pobranie próbek danych z https://bzp.uzp.gov.pl . Wystarczy 500–
1000 opisów przetargów.
Zadania
● Krok 1: czyszczenie danych
Usunięcie znaków specjalnych, tokenizacja (np. nltk, spaCy), etc.
● Krok 2: Analiza tekstu
Obliczenie liczby słów, długości zdań, liczby przymiotników /
rzeczowników (można użyć spacy-pl), etc.
● Krok 3: Model Markowa
Zbudowanie macierzy przejść między słowami (lub częściami mowy)
i na jej podstawie wygenerowanie 10 zamówień/opisów przetargów.
● Krok 4: System rekomendacyjny
na podstawie analizy tekstu, system powinien sugerować czy przetarg
dotyczy usługi, dostawy, czy robót budowlanych.
To można zrobić modelem regresji logistycznej lub naiwnym
modelem Bayesa.
● Krok 5: Raport
Krótki raport (5–10 stron) z opisem metod, wyników i wniosków.
Wymagane rezultaty do oddania
• Kod (Databricks Notebook).
• Raport PDF lub LaTex (ok. 6–10 stron, z wykresami i opisem
wyników).
• (Opcjonalnie) krótka prezentacja (5–7 slajdów).
