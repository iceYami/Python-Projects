public static string CaracterMasRepetido(string frase)
{
    Dictionary<char, int> contadorLetras = new Dictionary<char, int>();

    foreach (char letra in frase)
    {
        if (contadorLetras.ContainsKey(letra))
        {
            contadorLetras[letra]++;
        }
        else
        {
            contadorLetras.Add(letra, 1);
        }
    }

    int maxRepeticiones = contadorLetras.Values.Max();
    char caracterMasRepetido = contadorLetras.FirstOrDefault(x => x.Value == maxRepeticiones).Key;

    if (maxRepeticiones > 1)
    {
        int posicion = frase.IndexOf(caracterMasRepetido) + 1;
        return $"El carácter '{caracterMasRepetido}' se repite {maxRepeticiones} veces y aparece por primera vez en la posición {posicion}.";
    }
    else
    {
        return "Todos los caracteres de la frase aparecen por igual.";
    }
}
