# Desenvolvido por: Gabriel Martins Paz

"""
Mouse Virtual controlado por gestos das mãos via webcam.

Gestos:
- Apenas o indicador levantado  -> move o cursor (modo "mover")
- Indicador + médio levantados  -> clique esquerdo (ao aproximar as pontas)
- Polegar + indicador próximos  -> clique esquerdo (gesto de "pinça")
- Mão totalmente aberta parada  -> nenhuma ação

Pressione 'q' para fechar o programa.
"""

import cv2
import numpy as np
import time
import pyautogui

from hand_tracking_module import HandDetector

# ----------------------- CONFIGURAÇÕES -----------------------
CAM_WIDTH, CAM_HEIGHT = 640, 480       # resolução da captura da webcam
FRAME_REDUCTION = 100                  # margem (em px) que define a "área ativa" dentro do frame
SMOOTHENING = 5                        # suavização do movimento do cursor (maior = mais suave/lento)
CLICK_DISTANCE = 40                    # distância (px) entre dedos para considerar "clique"
CLICK_COOLDOWN = 0.3                   # tempo mínimo (s) entre cliques, evita clique duplicado

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Desativa a proteção de "canto da tela" do pyautogui (failsafe),
# pois o movimento por gestos pode levar o cursor até as bordas.
pyautogui.FAILSAFE = False


def main():
    prev_x, prev_y = 0, 0
    curr_x, curr_y = 0, 0
    last_click_time = 0
    is_dragging = False

    cap = cv2.VideoCapture(0)
    cap.set(3, CAM_WIDTH)
    cap.set(4, CAM_HEIGHT)

    detector = HandDetector(max_hands=1, detection_con=0.8, track_con=0.8)

    prev_time = 0

    print("Mouse virtual iniciado. Pressione 'q' na janela de vídeo para sair.")

    while True:
        success, img = cap.read()
        if not success:
            print("Não foi possível acessar a webcam.")
            break

        # Espelha a imagem para ficar mais intuitivo (como um espelho)
        img = cv2.flip(img, 1)

        img = detector.find_hands(img)
        lm_list = detector.find_position(img)

        # Desenha a "área ativa" (região que mapeia para a tela toda)
        cv2.rectangle(
            img,
            (FRAME_REDUCTION, FRAME_REDUCTION),
            (CAM_WIDTH - FRAME_REDUCTION, CAM_HEIGHT - FRAME_REDUCTION),
            (255, 0, 255),
            2,
        )

        if len(lm_list) != 0:
            # Ponta do indicador = landmark 8 | Ponta do polegar = landmark 4
            x_index, y_index = lm_list[8][1], lm_list[8][2]
            fingers = detector.fingers_up()

            # -------- MODO MOVER: apenas o indicador levantado --------
            if fingers[1] == 1 and fingers[2] == 0:
                # Converte coordenadas da área ativa da webcam para coordenadas da tela
                screen_x = np.interp(
                    x_index, (FRAME_REDUCTION, CAM_WIDTH - FRAME_REDUCTION), (0, SCREEN_WIDTH)
                )
                screen_y = np.interp(
                    y_index, (FRAME_REDUCTION, CAM_HEIGHT - FRAME_REDUCTION), (0, SCREEN_HEIGHT)
                )

                # Suaviza o movimento para evitar tremores/saltos bruscos
                curr_x = prev_x + (screen_x - prev_x) / SMOOTHENING
                curr_y = prev_y + (screen_y - prev_y) / SMOOTHENING

                pyautogui.moveTo(curr_x, curr_y)
                cv2.circle(img, (x_index, y_index), 10, (255, 0, 255), cv2.FILLED)

                prev_x, prev_y = curr_x, curr_y

            # -------- MODO CLIQUE: polegar + indicador próximos (gesto de pinça) --------
            if fingers[1] == 1 and fingers[0] == 1:
                length, img, line_info = detector.find_distance(4, 8, img)

                if length < CLICK_DISTANCE:
                    cv2.circle(img, (line_info[4], line_info[5]), 12, (0, 255, 0), cv2.FILLED)
                    now = time.time()
                    if now - last_click_time > CLICK_COOLDOWN:
                        pyautogui.click()
                        last_click_time = now

            # -------- MODO CLIQUE DIREITO: indicador + médio + anelar levantados --------
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[0] == 0:
                now = time.time()
                if now - last_click_time > CLICK_COOLDOWN:
                    pyautogui.rightClick()
                    last_click_time = now

        # Calcula e mostra o FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
        prev_time = curr_time
        cv2.putText(
            img, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2
        )

        cv2.imshow("Mouse Virtual - pressione 'q' para sair", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
