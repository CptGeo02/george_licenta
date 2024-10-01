import cv2

def draw_detections(frame, detections, table_info):
    for detection in detections:
        box = detection['box']
        class_id = detection['class']
        confidence = detection['confidence']

        x1, y1, x2, y2 = map(int, box)

        # Verificăm dacă este o persoană sau o masă
        if class_id == 0:
            color = (255, 0, 0)  # Albastru pentru oameni
            label = f"Om ({confidence:.2f})"
        elif class_id == 67:
            color = (0, 255, 0)  # Verde pentru mese
            label = f"Masă ({confidence:.2f})"
        else:
            continue

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Afișare informații mese
    for table_id, table_data in table_info.items():
        if 'bbox' in table_data:
            x1, y1, x2, y2 = table_data['bbox']  # Dacă există bbox, îl folosim
        else:
            # Dacă nu există 'bbox', folosește alt câmp sau gestionează eroarea
            print(f"Table {table_id} nu are bbox. Verifică structura.")
            continue

        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)  # Mov pentru mese
        cv2.putText(frame, f"Masă {table_id}: {table_data['status']}", (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    return frame
