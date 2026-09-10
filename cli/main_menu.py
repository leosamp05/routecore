while True:
    separator = "=" * 30
    
    print(separator)
    print("ROUTECORE".center(len(separator)))
    print(separator)
    print("1. Calcola Percorso")
    print("2. Aggiungi località")
    print("3. Aggiungi strada")
    print("4. Esci")
    try:
        choice = int(input("\nScelta: "))
    except ValueError:
        print("\nInserisci un numero valido.\n")
        continue
    
    if choice == 1:
        #altro menu
        pass
    
    elif choice == 2:
        pass
    
    elif choice == 3:
        pass
    
    elif choice == 4:
        break
    
    else:
        print("\nOpzione non valida\n\n")