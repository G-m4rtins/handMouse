"""
Módulo de rastreamento de mãos usando MediaPipe.
Detecta landmarks (pontos) das mãos e fornece funções auxiliares
para identificar posições dos dedos e distâncias entre eles.
"""

import cv2
import mediapipe as mp
import math


class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.7):
        """
        mode: se True, trata cada frame como imagem estática (mais lento, mais preciso)
        max_hands: número máximo de mãos detectadas simultaneamente
        detection_con: confiança mínima para detecção inicial
        track_con: confiança mínima para o rastreamento entre frames
        """
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con,
        )
        self.mp_draw = mp.solutions.drawing_utils

        # IDs dos dedos (ponta) no padrão MediaPipe:
        # 4 = polegar, 8 = indicador, 12 = médio, 16 = anelar, 20 = mínimo
        self.tip_ids = [4, 8, 12, 16, 20]

        self.results = None
        self.landmark_list = []

    def find_hands(self, img, draw=True):
        """Processa o frame e opcionalmente desenha os landmarks."""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, hand_lms, self.mp_hands.HAND_CONNECTIONS
                    )
        return img

    def find_position(self, img, hand_no=0):
        """Retorna a lista de landmarks [id, x, y] da mão detectada."""
        self.landmark_list = []

        if self.results and self.results.multi_hand_landmarks:
            if hand_no < len(self.results.multi_hand_landmarks):
                my_hand = self.results.multi_hand_landmarks[hand_no]
                h, w, _ = img.shape
                for lm_id, lm in enumerate(my_hand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.landmark_list.append([lm_id, cx, cy])

        return self.landmark_list

    def fingers_up(self):
        """
        Retorna uma lista de 5 posições (0 ou 1) indicando quais dedos
        estão levantados: [polegar, indicador, médio, anelar, mínimo]
        """
        fingers = []
        if not self.landmark_list:
            return [0, 0, 0, 0, 0]

        # Polegar: compara posição x (funciona melhor com mão espelhada pela webcam)
        if self.landmark_list[self.tip_ids[0]][1] > self.landmark_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Demais dedos: compara posição y da ponta com a articulação abaixo
        for finger_id in range(1, 5):
            tip = self.tip_ids[finger_id]
            if self.landmark_list[tip][2] < self.landmark_list[tip - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def find_distance(self, p1, p2, img=None, draw=True):
        """Calcula a distância euclidiana entre dois landmarks (ex: polegar e indicador)."""
        x1, y1 = self.landmark_list[p1][1], self.landmark_list[p1][2]
        x2, y2 = self.landmark_list[p2][1], self.landmark_list[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if img is not None and draw:
            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]


# Desenvolvido por: Gabriel Martins Paz
