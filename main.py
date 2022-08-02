# import cv2
# import os
# import glob
#
# # img = cv2.imread("galaxy.jpg", 1)
# # print(img.ndim)
# # print(img.shape)
#
# path = 'E:/Image AndVideoProcessingWithPython/sample_images'
# for filename in glob.glob(os.path.join(path, '*.jpg')):
#     with open(filename, 'r', encoding='utf-8'):
#         img = cv2.imread(filename, 1)
#         resized_img = cv2.resize(img,(int(img.shape[1]/2), int(img.shape[0]/2)))
#         cv2.imshow(f"{filename[52:len(filename)-4]}", resized_img)
#         cv2.imwrite(f"resized_{filename[52:]}", resized_img)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()

