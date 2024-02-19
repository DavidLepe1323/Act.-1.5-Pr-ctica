import re
import tkinter as tk
from tkinter import ttk

class AnalizadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.tokens = []

        # Definir patrones de expresiones regulares
        self.patrones = [
            ('IDENTIFICADOR', r'[a-zA-Z_]\w*'),
            ('PALABRA_RESERVADA', r'\b(?:if|else|while|for|return)\b'),
            ('TIPO_DATO', r'\b(?:int|float|bool|str)\b'),
            ('MAS', r'\+'),
            ('MENOS', r'\-'),
            ('IGUAL', r'='),
            ('MENOR', r'<'),
            ('MAYOR', r'>'),
            ('MENORIGUAL', r'<='),
            ('MAYORIGUAL', r'>='),
            ('IGUALIGUAL', r'=='),
            ('PARENTESIS_APERTURA', r'\('),
            ('PARENTESIS_CIERRE', r'\)'),
            ('LLAVE_APERTURA', r'\{'),
            ('LLAVE_CIERRE', r'\}'),
            ('PUNTOCOMA', r';'),
            ('DOSPUNTOS', r':'),
            ('OPERADOR_INCREMENTO', r'\+\+'),
            ('CORCHETE_APERTURA', r'\['),
            ('CORCHETE_CIERRE', r'\]')
        ]

    def analizar(self):
        tipos_patrones = set()
        for nombre_patron, patron in self.patrones:
            coincidencias = re.finditer(patron, self.codigo)
            for coincidencia in coincidencias:
                token = coincidencia.group()
                # Verificar si el token es palabra clave, tipo de dato o identificador
                if nombre_patron == 'PALABRA_RESERVADA' or nombre_patron == 'TIPO_DATO' or nombre_patron == 'IDENTIFICADOR':
                    tipo_token = nombre_patron
                else:
                    tipo_token = nombre_patron  # Usar el nombre del patrón como tipo para los demás casos
                self.tokens.append((token, tipo_token))
                tipos_patrones.add(tipo_token)

        return tipos_patrones

    def analizar_linea(self, linea):
        tokens_linea = []
        for nombre_patron, patron in self.patrones:
            coincidencias = re.finditer(patron, linea)
            for coincidencia in coincidencias:
                token = coincidencia.group()
                # Verificar si el token es palabra clave, tipo de dato o identificador
                if nombre_patron == 'PALABRA_RESERVADA' or nombre_patron == 'TIPO_DATO' or nombre_patron == 'IDENTIFICADOR':
                    tipo_token = nombre_patron
                else:
                    tipo_token = nombre_patron  # Usar el nombre del patrón como tipo para los demás casos
                tokens_linea.append((token, tipo_token))
        return tokens_linea

class InterfazLexer:
    def __init__(self, master):
        self.master = master
        self.master.title("Analizador Léxico")

        # Configuración del frame principal
        self.marco_principal = ttk.Frame(self.master)
        self.marco_principal.pack(padx=10, pady=10)

        # Configuración del área de texto para el código
        self.texto_codigo = tk.Text(self.marco_principal, height=10, width=40)
        self.texto_codigo.grid(row=0, column=0, padx=5, pady=5)

        # Configuración del botón de análisis
        self.boton_analizar = tk.Button(self.marco_principal, text="Analizar", command=self.analizar)
        self.boton_analizar.grid(row=1, column=0, pady=5)

        # Configuración de la tabla
        self.marco_tabla = ttk.Frame(self.marco_principal)
        self.marco_tabla.grid(row=2, column=0, pady=10)

        self.tabla = ttk.Treeview(self.marco_tabla, columns=('Línea', 'Token', 'Tipo'), show='headings')
        self.tabla.heading('Línea', text='Línea')
        self.tabla.heading('Token', text='Token')
        self.tabla.heading('Tipo', text='Tipo')
        self.tabla.pack()

    def analizar(self):
        codigo = self.texto_codigo.get("1.0", "end-1c")
        analizador = AnalizadorLexico(codigo)
        tipos_patrones = analizador.analizar()

        # Limpiar la tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Enumerar las líneas y procesar cada línea
        for i, linea in enumerate(codigo.split('\n'), start=1):
            # Analizar tokens de la línea
            tokens_linea = analizador.analizar_linea(linea)

            # Mostrar tokens en la tabla
            self.mostrar_tabla(i, tokens_linea)

    def mostrar_tabla(self, numero_linea, tokens):
        for token, tipo_token in tokens:
            self.tabla.insert('', 'end', values=(numero_linea, token, tipo_token))

if __name__ == "__main__":
    root = tk.Tk()
    gui = InterfazLexer(root)
    root.mainloop()
