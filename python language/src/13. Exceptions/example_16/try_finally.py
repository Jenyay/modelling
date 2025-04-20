try:
    print("Вошли в блок try.")
    raise OSError()
    print("Выходим из блока try.")
except ValueError:
    print("Вошли в блок except.")
else:
    print("Вошли в блок else.")
finally:
    print("Вошли в блок finally.")

print("Вышли из блока try / except / else / finally.")
