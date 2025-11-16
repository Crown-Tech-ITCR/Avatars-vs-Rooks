# 🎮 Integración Raspberry Pi Pico W con Avatars vs Rooks

## 📋 Descripción General

Este sistema permite controlar el juego con un **mando inalámbrico WiFi** usando tu Raspberry Pi Pico W. El juego funciona con tres modos de entrada automáticos:

### 🎯 Sistema de Prioridad Automático

1. **🎮 Mando WiFi** (Raspberry Pi Pico W) - Si está encendido y conectado
2. **🕹️ Mando USB** (Raspberry Pi Pico por serial) - Si está conectado por cable
3. **⌨️ Teclado/Mouse** - Si no hay ningún mando conectado

**¡El juego detecta automáticamente qué está disponible y funciona sin problemas!**

## ✨ Características

- ✅ **Control transparente**: El juego funciona igual sin importar el método de entrada
- ✅ **Sin configuración manual**: Conexión automática al iniciar el juego
- ✅ **Siempre funcional**: Si el mando no está disponible, usa teclado
- ✅ **Comunicación bidireccional**: El juego envía información al mando (LEDs, displays, etc.)
- ✅ **Compatible con hardware existente**: Funciona con tu sistema actual de InputHandler

## 📁 Archivos Creados

1. **`pico_communication.py`** - Cliente WiFi para comunicación con la Pico W
2. **`wifi_handler.py`** - Adaptador que integra WiFi con InputHandler
3. **`pico_main.py`** - Código para la Raspberry Pi Pico W (MicroPython)
4. **`pico_integration_example.py`** - Ejemplos y pruebas (opcional)

**El juego ya está integrado** - Solo necesitas configurar la IP de tu Pico W.

---

## ⚡ Inicio Rápido (Mando Inalámbrico con Batería)

### 🎯 Lo Esencial

**Para usar tu Pico W como mando inalámbrico sin cables:**

1. **Alimentación: Power Bank + Cable USB**
   ```
   Power Bank → Cable USB Micro-B → Pico W
   ```
   *(Es el mismo cable que usas para programarla)*

2. **¿Se enciende sola?**
   - **SÍ** - Al conectar la batería, la Pico W arranca automáticamente
   - Ejecuta `main.py` automáticamente
   - Se conecta al WiFi sola
   - ¡Lista para jugar!

3. **Pines de batería** (si usas baterías AA en lugar de power bank):
   ```
   Batería (+) → Pin 39 (VSYS)
   Batería (-) → Pin GND (cualquier GND)
   ```
   *Usa máximo 3 baterías AA (4.5V)*

**Ver más detalles en la sección [🔋 Alimentación con Batería](#-alimentación-con-batería-mando-inalámbrico)**

---

## 🚀 Guía de Instalación

### Paso 1: Configurar la Raspberry Pi Pico W

#### 1.1. Instalar MicroPython en la Pico W

1. Descarga el firmware de MicroPython para Pico W desde:
   https://micropython.org/download/rp2-pico-w/
   
2. Mantén presionado el botón BOOTSEL de la Pico W y conéctala al USB

3. Arrastra el archivo `.uf2` descargado a la unidad `RPI-RP2` que aparece

4. La Pico W se reiniciará automáticamente

#### 1.2. Instalar Thonny IDE

1. Descarga Thonny desde: https://thonny.org/

2. Instala y abre Thonny

3. Ve a `Tools > Options > Interpreter`

4. Selecciona "MicroPython (Raspberry Pi Pico)"

5. Selecciona el puerto COM de tu Pico W

#### 1.3. Subir el código a la Pico W

1. Abre `pico_main.py` en Thonny

2. **IMPORTANTE:** Modifica estas líneas con tus datos:
   ```python
   WIFI_SSID = "TU_WIFI_AQUI"          # Tu red WiFi
   WIFI_PASSWORD = "TU_PASSWORD_AQUI"   # Tu contraseña WiFi
   ```

3. Ve a `File > Save As...`

4. Selecciona "Raspberry Pi Pico"

5. Guarda como `main.py`

6. Desconecta y reconecta la Pico W para que se ejecute automáticamente

7. En la consola de Thonny verás:
   ```
   ✓ Conectado a WiFi
   ✓ IP de la Pico W: 192.168.1.XXX
   ✓ Puerto: 8080
   
   >>> Usa esta IP en tu juego: 192.168.1.XXX <<<
   ```

8. **¡ANOTA ESTA IP!** La necesitarás para el juego

---

### Paso 2: Configurar el Juego (PC)

#### 2.1. Configurar la IP de tu Pico W

1. Abre `game_interface.py`

2. Busca la línea (~línea 187):
   ```python
   PICO_IP = "192.168.1.100"  # ← MODIFICAR CON TU IP
   ```

3. Reemplaza `192.168.1.100` con la IP que anotaste de tu Pico W

4. Guarda el archivo

**¡Eso es todo! El juego detectará automáticamente el mando WiFi al iniciar.**

#### 2.2. Probar el sistema

1. **Asegúrate de que la Pico W esté encendida** y conectada a WiFi

2. **Ejecuta el juego**:
   ```bash
   python main.py
   ```

3. Al iniciar el juego, verás uno de estos mensajes:

   - **Mando WiFi detectado**:
     ```
     🎮 Buscando mando WiFi en 192.168.1.XXX:8080...
     ✓ Mando WiFi conectado - Controles del mando activados
     ✓ Mando WiFi integrado con InputHandler
     ✓ Sistema de entrada: MANDO WiFi
     ```

   - **Mando no detectado** (el juego funciona igual con teclado):
     ```
     🎮 Buscando mando WiFi en 192.168.1.XXX:8080...
     ⌨️  Mando WiFi no detectado - Usando teclado
     ✓ Sistema de entrada: TECLADO/MOUSE
     ```

4. **Si el mando WiFi está conectado**, verás el LED de la Pico W parpadear brevemente

5. **Usa el joystick del mando** para mover el cursor en el juego

6. **Presiona los botones** para seleccionar y colocar rooks

---

## 🎮 Cómo Funciona

### Flujo de Conexión

```
┌─────────────────────────────────────────────────┐
│  INICIO DEL JUEGO                               │
└──────────────┬──────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────┐
│  ¿Mando WiFi encendido y conectado?             │
└──────────────┬──────────────────────────────────┘
               │
       ┌───────┴───────┐
       │               │
      SÍ              NO
       │               │
       ▼               ▼
┌─────────────┐  ┌─────────────────────────┐
│ MANDO WiFi  │  │ ¿Mando USB conectado?   │
│   ACTIVO    │  └──────────┬──────────────┘
└─────────────┘             │
                    ┌───────┴───────┐
                    │               │
                   SÍ              NO
                    │               │
                    ▼               ▼
              ┌─────────────┐  ┌──────────────┐
              │  MANDO USB  │  │ TECLADO/     │
              │   ACTIVO    │  │   MOUSE      │
              └─────────────┘  └──────────────┘
```

### Comunicación en Tiempo Real

```
┌──────────────────┐         WiFi         ┌───────────────────┐
│                  │ ◄─────────────────► │                   │
│   PC (Juego)     │                      │  Raspberry Pi     │
│                  │   Joystick/Botones   │    Pico W         │
│  • Python        │ ◄──────────────────  │  • MicroPython    │
│  • Tkinter       │                      │  • GPIO           │
│  • game_logic    │   Estado del Juego   │  • LEDs           │
│  • InputHandler  │  ────────────────►   │  • Sensores       │
│                  │                      │                   │
└──────────────────┘                      └───────────────────┘
```

### Comandos del Mando al Juego

**Joystick:**
- Formato: `"Direccion,Click"`
- Ejemplos: `"Arriba,0"`, `"Centro,1"`, `"Izquierda,0"`

**Botones de Rook:**
- Formato: `"BTN,TIPO"`
- Ejemplos: `"BTN,ARENA"`, `"BTN,FUEGO"`, `"BTN,AGUA"`, `"BTN,ROCA"`

**Todos estos comandos son procesados automáticamente por `InputHandler`**

---

## 🔋 Alimentación con Batería (Mando Inalámbrico)

### ¿Cómo alimentar la Pico W sin la computadora?

La Raspberry Pi Pico W tiene **3 formas** de recibir energía:

#### **Opción 1: Cable USB + Power Bank (Más Fácil) ⭐ RECOMENDADO**

**Lo que necesitas:**
- 1× Power Bank (batería externa de celular)
- 1× Cable USB Micro-B (el mismo que usas para programarla)

**Conexión:**
```
Power Bank → Cable USB → Puerto Micro-USB de la Pico W
```

**Ventajas:**
- ✅ Súper fácil, no necesitas soldar nada
- ✅ Puedes usar cualquier power bank que tengas
- ✅ Voltaje regulado automáticamente (5V)
- ✅ Puedes recargar el power bank

**¿Cómo funciona?**
1. Conecta el cable USB del power bank a la Pico W
2. Enciende el power bank
3. La Pico W arranca automáticamente y ejecuta `main.py`
4. Se conecta al WiFi automáticamente
5. ¡Listo! Ya puedes jugar sin cable a la PC

---

#### **Opción 2: Baterías AA/AAA + Regulador de Voltaje**

**Lo que necesitas:**
- 3× Baterías AA o AAA (total: 4.5V)
- 1× Portapilas para 3 baterías
- Cables para conectar

**Conexión:**
```
Portapilas (+) → Pin VSYS (Pin 39)
Portapilas (-) → Pin GND (cualquier pin GND)
```

**⚠️ IMPORTANTE:**
- La Pico W acepta de **1.8V a 5.5V** en el pin VSYS
- Con 3 baterías AA nuevas tienes ~4.5V (perfecto)
- **NO uses más de 3 baterías** (podrías dañar la Pico W)

**Ubicación de los pines:**
```
        Raspberry Pi Pico W (Vista Superior)
        
    USB [▓▓▓▓▓▓▓▓]
        
    Pin 1  [ ]  [ ] Pin 40 (VBUS) ← NO usar con batería
    Pin 2  [ ]  [ ] Pin 39 (VSYS) ← BATERÍA (+) AQUÍ
    Pin 3  [ ]  [ ] Pin 38 (GND)  ← BATERÍA (-) AQUÍ (o cualquier GND)
    Pin 4  [ ]  [ ] Pin 37
    Pin 5  [ ]  [ ] Pin 36
    Pin 6  [ ]  [ ] Pin 35
    Pin 7  [ ]  [ ] Pin 34
    Pin 8  [ ]  [ ] Pin 33 (GND)  ← También puedes usar este GND
           ...
    Pin 20 [ ]  [ ] Pin 21
    
    CONEXIÓN DE BATERÍA:
    ────────────────────────────────────────
    Batería (+) rojo    →  Pin 39 (VSYS)
    Batería (-) negro   →  Pin 38 o 33 (GND)
    
    VOLTAJE PERMITIDO: 1.8V - 5.5V
    RECOMENDADO: 3-4.5V (2-3 baterías AA)
```

**Consejos de conexión:**
- Usa cables con terminales Dupont hembra para conectar a los pines
- Puedes soldar los cables directamente si quieres algo más permanente
- Agrega un interruptor en el cable positivo para encender/apagar fácilmente

---

#### **Opción 3: Batería LiPo 3.7V (Para Proyectos Avanzados)**

**Lo que necesitas:**
- 1× Batería LiPo 3.7V (1000-2000 mAh recomendado)
- Cables JST o soldar directamente

**Conexión:**
```
Batería (+) → Pin VSYS (Pin 39)
Batería (-) → Pin GND
```

**⚠️ Precauciones:**
- Las baterías LiPo requieren cargadores especiales
- Nunca descargues por debajo de 3.0V
- Son más peligrosas si no se manejan correctamente

---

### 🚀 Inicio Automático al Encender

**¡Buenas noticias!** La Pico W ya está configurada para inicio automático:

1. **El archivo `main.py`** se ejecuta automáticamente al encender
2. **Se conecta al WiFi** automáticamente
3. **Inicia el servidor** y queda esperando conexiones
4. **¡Ya está lista para jugar!**

**No necesitas hacer NADA adicional** - solo conectar la batería.

---

### 🔌 Diagrama de Conexión Completa (Opción Power Bank)

```
┌─────────────────────────────────────────────────────────────┐
│                     MANDO INALÁMBRICO                        │
│                                                              │
│  ┌──────────────┐        USB Cable      ┌────────────────┐ │
│  │  Power Bank  │━━━━━━━━━━━━━━━━━━━━━▶│  Pico W        │ │
│  │  (Batería)   │      Micro-USB        │                │ │
│  └──────────────┘                       │  ┌──────────┐  │ │
│                                          │  │ Joystick │  │ │
│                                          │  └────┬─────┘  │ │
│                                          │       │        │ │
│                                          │  ┌────┴─────┐  │ │
│                                          │  │ Botones  │  │ │
│                                          │  └──────────┘  │ │
│                                          │  ┌──────────┐  │ │
│                                          │  │ Buzzer   │  │ │
│                                          │  └──────────┘  │ │
│                                          └────────────────┘ │
│                                                              │
│                          WiFi (Inalámbrico)                  │
│                                 ▼                            │
│                          ┌──────────┐                        │
│                          │  Router  │                        │
│                          └─────┬────┘                        │
│                                │                             │
│                                ▼                             │
│                          ┌──────────┐                        │
│                          │    PC    │                        │
│                          │ (Juego)  │                        │
│                          └──────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

---

### ⚡ Duración de la Batería

**Con un Power Bank típico de 10,000 mAh:**

- Pico W consume ~150mA jugando (WiFi + LEDs + Buzzer)
- Duración aproximada: **60-65 horas** de juego continuo
- En práctica: **varios días** de uso normal

**Consejos para ahorrar batería:**
- El LED integrado consume poco, puedes dejarlo
- El WiFi es el que más consume (pero lo necesitas)
- Apaga el mando cuando no lo uses

---

### ❓ Preguntas Frecuentes sobre Batería

**P: ¿Se borra el código si desconecto la batería?**
R: **NO** - El código está guardado en la memoria flash de la Pico W. Solo se ejecuta cuando tiene energía.

**P: ¿Puedo programarla mientras está con batería?**
R: **SÍ** - Puedes conectar el USB de la PC mientras tiene batería. La Pico W usa automáticamente la fuente USB si está conectada.

**P: ¿Cómo sé que está encendida?**
R: El **LED integrado** parpadea al conectarse al WiFi. También puedes ver la conexión en la consola del juego.

**P: ¿Necesito un interruptor?**
R: **Opcional** - Puedes agregar un interruptor entre la batería y el pin VSYS para encender/apagar fácilmente.

**P: ¿Puedo usar 4 baterías AA?**
R: **NO RECOMENDADO** - 4 × 1.5V = 6V, que está por encima del límite seguro (5.5V). Usa máximo 3 baterías.

**P: Mi power bank se apaga solo, ¿por qué?**
R: Algunos power banks se apagan con consumos bajos. Busca uno con "modo de baja corriente" o agrega una resistencia de carga.

---

### 🎮 Primer Uso: Paso a Paso Completo

**Para la primera vez que uses el mando inalámbrico:**

#### 1️⃣ Programar la Pico W (Solo una vez)

1. **Conecta la Pico W a la PC con cable USB**
2. **Abre Thonny** y verifica que esté conectada
3. **Sube estos archivos** a la Pico W:
   - `pico_main.py` (guárdalo como `main.py`)
   - `Joystick.py`
   - `Buzzer.py`
   - `Botones.py`
4. **Anota la IP** que muestra en la consola (ej: `192.168.1.150`)
5. **Desconecta el cable USB**

#### 2️⃣ Configurar el Juego en la PC (Solo una vez)

1. **Abre** `game_interface.py` en VS Code
2. **Busca la línea ~187**: `PICO_IP = "192.168.1.100"`
3. **Cámbiala** por la IP de tu Pico W: `PICO_IP = "192.168.1.150"`
4. **Guarda** el archivo

#### 3️⃣ Conectar la Batería (Cada vez que juegues)

**Opción fácil - Power Bank:**
```
1. Conecta el cable USB del power bank a la Pico W
2. Enciende el power bank
3. ¡Listo! La Pico W arranca sola
```

**Opción baterías AA:**
```
1. Pon 3 baterías AA en el portapilas
2. Conecta cable rojo (+) a Pin 39 (VSYS)
3. Conecta cable negro (-) a Pin 38 (GND)
4. ¡Listo! La Pico W arranca sola
```

#### 4️⃣ Verificar que Funciona

1. El **LED de la Pico W** debe parpadear 3 veces (iniciando)
2. Después parpadea conectándose al WiFi
3. **Queda encendido fijo** cuando está conectado
4. En Thonny puedes ver: `"✓ Conectado a WiFi"` y `"✓ IP: 192.168.1.XXX"`

#### 5️⃣ Jugar

1. **En tu PC, ejecuta**: `python main.py`
2. **Verás**: `✓ Mando WiFi conectado`
3. **¡A jugar!** 🎮

---

### 🔄 Usos Posteriores

**Para los siguientes usos es mucho más simple:**

1. ✅ Conecta la batería a la Pico W
2. ✅ Espera 5-10 segundos (se conecta al WiFi)
3. ✅ Ejecuta el juego en la PC: `python main.py`
4. ✅ ¡Juega!

**No necesitas reprogramar nada ni reconectar por USB.**

---

## 🔌 Conexiones de Hardware (Opcional)

### Agregar Botones Físicos

Si quieres agregar botones a tu Pico W:

**Materiales:**
- 2 botones pulsadores
- 2 resistencias de 10kΩ (opcional si usas pull-up interno)
- Cables jumper
- Protoboard

**Conexión:**
```
Botón A:
  Pin 14 (GPIO14) → Botón → GND
  
Botón B:
  Pin 15 (GPIO15) → Botón → GND
```

**Código en pico_main.py:**

Descomenta estas líneas (aprox. línea 26):
```python
button_a = Pin(14, Pin.IN, Pin.PULL_UP)
button_b = Pin(15, Pin.IN, Pin.PULL_UP)
```

Y en la función `check_buttons()` (aprox. línea 154):
```python
def check_buttons(client_socket):
    if button_a.value() == 0:  # Botón presionado
        send_event(client_socket, "button_press", {"button": "A"})
        time.sleep(0.3)  # Debounce
    
    if button_b.value() == 0:
        send_event(client_socket, "button_press", {"button": "B"})
        time.sleep(0.3)
```

---

## 📡 Comunicación Juego ↔ Mando

### Del Juego → Mando WiFi (Automático)

El juego envía automáticamente estos comandos al mando:

| Comando | Cuándo | Descripción |
|---------|--------|-------------|
| `game_state` | Cada actualización | Estado del juego (nivel, puntos, vidas) |
| `led_blink` | Nivel completado | LED parpadea en celebración |
| `game_over` | Fin del juego | Notifica victoria o derrota |

**Puedes agregar más comandos personalizados si quieres** (ver sección de personalización).

### Del Mando → Juego (Automático)

El mando envía automáticamente:

| Evento | Datos | Descripción |
|--------|-------|-------------|
| `joystick` | `{comando: "Arriba,0"}` | Movimiento del joystick |
| `button` | `{comando: "BTN,FUEGO"}` | Botón de rook presionado |

**Estos eventos son procesados automáticamente por `InputHandler` - ¡no necesitas código adicional!**

---

## 🧪 Pruebas

### Prueba 1: Verificar Conexión

1. **Enciende tu Pico W** (debe mostrar su IP en Thonny)

2. **Inicia el juego**:
   ```bash
   python main.py
   ```

3. **Busca el mensaje en la consola**:
   ```
   🎮 Buscando mando WiFi en 192.168.1.XXX:8080...
   ✓ Mando WiFi conectado - Controles del mando activados
   ```

4. **Verifica el LED** de la Pico W - debe parpadear brevemente

### Prueba 2: Control con Joystick

1. **Inicia un nivel** del juego

2. **Mueve el joystick** en tu mando

3. **El cursor debe moverse** en el tablero del juego

4. **Presiona el botón del joystick** - debe colocar un rook

### Prueba 3: Botones de Rook

1. **Presiona los botones físicos** (Arena, Roca, Fuego, Agua)

2. **El juego debe seleccionar** el rook correspondiente

3. **Verifica en la consola** que los comandos se reciben

### Prueba 4: Juego sin Mando (Fallback)

1. **Apaga la Pico W**

2. **Inicia el juego**:
   ```bash
   python main.py
   ```

3. **Debe aparecer**:
   ```
   🎮 Buscando mando WiFi en 192.168.1.XXX:8080...
   ⌨️  Mando WiFi no detectado - Usando teclado
   ✓ Sistema de entrada: TECLADO/MOUSE
   ```

4. **El juego funciona normal** con teclado y mouse

---

## ❓ Solución de Problemas

### Error: "Mando WiFi no detectado"

**Esto NO es un error** - simplemente significa que el juego usará teclado/mouse. Si quieres usar el mando WiFi:

1. **Verifica que la Pico W esté encendida**
   - El LED debe estar encendido o parpadeando
   - Verifica en Thonny que `main.py` se esté ejecutando

2. **Verifica la IP en `game_interface.py`**
   - La IP debe coincidir con la que muestra tu Pico W
   - Busca la línea: `PICO_IP = "192.168.1.100"`

3. **Verifica que estén en la misma red WiFi**
   - PC y Pico W deben estar conectados a la misma red
   - Verifica el SSID en ambos dispositivos

4. **Verifica el firewall**
   - Windows puede bloquear Python
   - Ve a: Firewall → Permitir una aplicación → Python
   - O desactiva temporalmente el firewall para probar

### Joystick no responde

1. **Verifica las conexiones físicas**:
   ```
   Joystick VRx → GP26 (ADC0)
   Joystick VRy → GP27 (ADC1)
   Joystick SW  → GP14 (con pull-up)
   ```

2. **Prueba el joystick en Thonny**:
   ```python
   from machine import Pin, ADC
   x = ADC(Pin(26))
   print(x.read_u16())  # Debe mostrar ~32768 en centro
   ```

3. **Ajusta la zona muerta** en `pico_main.py`:
   ```python
   JOYSTICK_DEADZONE = 15000  # Aumenta si es muy sensible
   ```

### Botones no funcionan

1. **Verifica las conexiones** (con pull-up, activo en bajo):
   ```
   Botón ARENA → GP15 → GND
   Botón ROCA  → GP16 → GND
   Botón FUEGO → GP17 → GND
   Botón AGUA  → GP18 → GND
   ```

2. **Verifica que estén habilitados** en `pico_main.py`:
   ```python
   BUTTONS_ENABLED = True  # Debe ser True
   ```

3. **Prueba en Thonny**:
   ```python
   from machine import Pin
   btn = Pin(15, Pin.IN, Pin.PULL_UP)
   print(btn.value())  # 1=no presionado, 0=presionado
   ```

### LED no responde

El LED integrado de la Pico W es `Pin("LED", Pin.OUT)` - está correcto en el código.

### Conexión se pierde durante el juego

1. **Verifica la alimentación** - USB de calidad o fuente de 5V estable
2. **Verifica la señal WiFi** - acerca la Pico W al router
3. **Reinicia la Pico W** - desconecta y reconecta

---

## 🎨 Personalización

### Agregar Nuevos Comandos

**En pico_main.py (Pico W):**
```python
def handle_command(command_dict, client_socket):
    # ... código existente ...
    
    elif command == "mi_comando":
        data = data.get("mi_dato")
        print(f"Mi comando recibido: {data}")
        # Tu código aquí
```

**En el juego:**
```python
self.pico.send_command("mi_comando", {"mi_dato": "valor"})
```

### Agregar Nuevos Eventos

**En pico_main.py (Pico W):**
```python
send_event(client_socket, "mi_evento", {"valor": 123})
```

**En el juego:**
```python
self.pico.on_event("mi_evento", self.mi_callback)

def mi_callback(self, data):
    print(f"Mi evento: {data}")
```

---

## 📊 Diagrama de Comunicación

```
┌─────────────────┐                    ┌──────────────────┐
│                 │   WiFi TCP/IP      │                  │
│   PC (Juego)    │ ←──────────────→   │  Raspberry Pi    │
│                 │    Puerto 8080     │    Pico W        │
│                 │                    │                  │
│ • Python        │  → Comandos        │ • MicroPython    │
│ • Tkinter       │  ← Eventos         │ • GPIO           │
│ • game_logic    │                    │ • LED/Botones    │
└─────────────────┘                    └──────────────────┘
```

---

## 📝 Notas Importantes

- ✅ El juego **siempre funciona** - con o sin mando WiFi
- ✅ Detección **automática** al iniciar el juego
- ✅ Sistema de **prioridad**: WiFi → USB → Teclado
- ✅ Comunicación **no bloqueante** - usa hilos (threads)
- ✅ Compatible con tu sistema **InputHandler** existente
- ✅ El código de la Pico W (`pico_main.py`) **solo se ejecuta en la Pico W**, no en tu PC
- ⚠️ Los errores de import en `pico_main.py` son **normales** - ese archivo es para MicroPython

### Cambiar la IP del Mando

Si cambias de red WiFi o la IP de la Pico W cambia:

1. Abre `game_interface.py`
2. Busca la línea (~180): `PICO_IP = "192.168.1.100"`
3. Actualiza con la nueva IP
4. Reinicia el juego

---

## 🎨 Personalización

### Agregar Comandos Personalizados al Mando

**En `pico_main.py` (Pico W):**
```python
def handle_command(command_dict, client_socket):
    # ... código existente ...
    
    elif command == "mi_comando_personalizado":
        data = command_dict.get("data", {})
        # Tu código aquí
        print(f"Comando personalizado: {data}")
```

**En `game_interface.py` (Juego):**
```python
# Enviar desde cualquier parte del juego
if self.wifi_handler and self.wifi_handler.is_connected():
    self.wifi_handler.pico.send_command("mi_comando_personalizado", {
        "mi_dato": "valor"
    })
```

### Agregar Más Botones

1. **Conecta el botón** a un pin GPIO libre (con pull-up)
2. **En `pico_main.py`**, agrega:
   ```python
   button_nuevo = Pin(19, Pin.IN, Pin.PULL_UP)  # GP19
   ```
3. **En `verificar_botones_rook()`**, agrega:
   ```python
   (button_nuevo, "NUEVO"),
   ```
4. El juego procesará automáticamente `"BTN,NUEVO"`

### Agregar Display LCD o LEDs RGB

Puedes agregar displays, LEDs RGB, buzzers, etc. simplemente:

1. **Conecta el hardware** a pines libres de la Pico W
2. **Agrega el código** en `handle_command()` para procesar comandos
3. **Envía comandos desde el juego** cuando quieras actualizar el display

**Ejemplo - Display LCD 16x2:**
```python
# En pico_main.py
from machine import I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

def handle_command(command_dict, client_socket):
    # ... código existente ...
    
    elif command == "update_display":
        line1 = data.get("line1", "")
        line2 = data.get("line2", "")
        lcd.clear()
        lcd.putstr(line1 + "\n" + line2)
```

```python
# En game_interface.py - enviar estado al display
if self.wifi_handler and self.wifi_handler.is_connected():
    self.wifi_handler.pico.send_command("update_display", {
        "line1": f"Nivel: {self.nivel}",
        "line2": f"Puntos: {self.puntos}"
    })
```

---

## 📄 Licencia

Este código es parte del proyecto Avatars vs Rooks.

---

## 🎯 Resumen Rápido

### Para usar el mando WiFi:

1. ✅ Sube `pico_main.py` a tu Pico W con tus credenciales WiFi
2. ✅ Anota la IP que muestra en Thonny
3. ✅ Actualiza `PICO_IP` en `game_interface.py` (~línea 180)
4. ✅ Conecta tu joystick y botones a la Pico W
5. ✅ ¡Juega!

### Si el mando no está:

- ⌨️ El juego funciona automáticamente con teclado/mouse
- 🎮 Sin configuración adicional necesaria
- ✅ Todo sigue funcionando perfectamente

**¡Disfruta tu juego con control inalámbrico!** 🚀
