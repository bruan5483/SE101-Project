import cv2

cap = cv2.VideoCapture(2)

# # Test up to 10 indices (modify as needed)
# for i in range(2, 10):
#     cap = cv2.VideoCapture(i)
    
#     if cap.isOpened():
#         print(f"Camera found on index {i}")
#         ret, frame = cap.read()
        
#         if ret:
#             cv2.imshow(f'Camera {i}', frame)
#             cv2.waitKey(1000)  # Display the frame for 1 second
#             cv2.destroyAllWindows()
        
#         cap.release()
#     else:
#         print(f"No camera found on index {i}")
