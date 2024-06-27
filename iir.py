import pyaudio
import numpy as np
import scipy.signal as signal
import soundfile as sf
import os

def grabacion():
    # Parámetros de grabación
    fs = 100000  # Frecuencia de muestreo (Hz) aumentada para mejor calidad
    nBits = 16  # Número de bits por muestra
    nChannels = 1  # Número de canales (1 para mono)
    duration = 5  # Duración de la grabación (segundos)

    # Configuración de PyAudio
    p = pyaudio.PyAudio()

    # Iniciar la grabación
    print("Comenzando la grabación de audio...")
    stream = p.open(format=pyaudio.paInt16, channels=nChannels, rate=fs, input=True, frames_per_buffer=1024)
    frames = []

    for i in range(0, int(fs / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Grabación finalizada.")

    # Detener la grabación
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convertir los datos a un array de numpy
    audioData = np.frombuffer(b''.join(frames), dtype=np.int16)

    if len(audioData) == 0:
        raise ValueError('No se capturaron datos de audio. Verifica tu micrófono y los permisos de grabación.')
    else:
        # print('Datos de audio capturados exitosamente.')
        pass

    # Parámetros del filtro
    fc = 1400  # Frecuencia central (Hz)
    bw = 200  # Ancho de banda del filtro (Hz)
    order = 4  # Orden del filtro

    # Calcular las frecuencias de corte normalizadas
    f1 = (fc - bw / 2) / (fs / 2)  # Frecuencia de corte baja normalizada
    f2 = (fc + bw / 2) / (fs / 2)  # Frecuencia de corte alta normalizada

    # Verificar que las frecuencias estén dentro del rango permitido
    if not (0 < f1 < 1 and 0 < f2 < 1):
        raise ValueError(f'Las frecuencias de corte deben estar entre 0 y 1 después de la normalización. f1: {f1}, f2: {f2}')

    # Diseñar el filtro Butterworth pasa banda
    b, a = signal.butter(order, [f1, f2], btype='band')

    # Aplicar el filtro a la señal de audio capturada
    filteredAudio = signal.lfilter(b, a, audioData)

    # Normalizar el audio filtrado para evitar distorsión
    filteredAudio = filteredAudio / np.max(np.abs(filteredAudio), axis=0)

    # Guardar el audio filtrado
    filename = '8.wav'
    sf.write(filename, filteredAudio, fs)

    if os.path.exists(filename):
        pass
        # print(f'El audio filtrado ha sido guardado en {filename}')
    else:
        raise IOError('Error al guardar el archivo de audio.')
