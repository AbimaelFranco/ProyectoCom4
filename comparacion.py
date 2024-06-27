import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import freqz, correlate
import pyaudio
import wave

# Función para reproducir audio
def reproducir_audio(filename):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

# Función para calcular la frecuencia dominante
def calcular_frecuencia_dominante(audio, fs):
    N = len(audio)
    fft_result = np.fft.fft(audio)
    fft_magnitude = np.abs(fft_result[:N // 2 + 1])
    frequencies = np.fft.fftfreq(N, d=1/fs)[:N // 2 + 1]
    dominant_frequency = frequencies[np.argmax(fft_magnitude)]
    return dominant_frequency

# Función para comparar frecuencias dominantes con tolerancia
def comparar_frecuencias(audio_ref, fs_ref, audio_comp, fs_comp, tolerancia=3.0):
    frecuencia_dominante_audio_ref = calcular_frecuencia_dominante(audio_ref, fs_ref)
    frecuencia_dominante_audio_comp = calcular_frecuencia_dominante(audio_comp, fs_comp)
    
    if abs(frecuencia_dominante_audio_ref - frecuencia_dominante_audio_comp) <= tolerancia:
        return True
    else:
        return False

# Archivos de audio a comparar
archivos_audio = ['filteredAudio1.wav', 'filteredAudio2.wav', 'filteredAudio3.wav']
audio_referencia = '8.wav'  # Audio de referencia para comparación
tolerancia = 5.0  # Tolerancia para la comparación de frecuencias (±3 Hz)

# Cargar audio de referencia
audio_ref, fs_ref = sf.read(audio_referencia)

# Comparar cada archivo con el audio de referencia y mostrar resultados
for archivo in archivos_audio:
    audio_comp, fs_comp = sf.read(archivo)
    
    if comparar_frecuencias(audio_ref, fs_ref, audio_comp, fs_comp, tolerancia):
        print(f"El archivo {archivo} tiene una frecuencia dominante similar dentro de la tolerancia de ±{tolerancia} Hz.")
    else:
        print(f"El archivo {archivo} no tiene una frecuencia dominante similar dentro de la tolerancia de ±{tolerancia} Hz.")
    
    # Reproducir el audio comparado
    print(f"Reproduciendo Archivo de audio: {archivo}")
    reproducir_audio(archivo)
