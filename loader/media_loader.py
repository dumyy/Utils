import cv2
import os
import glob

class ImageLoader():
    def __init__(self, base_path, suffix='png') -> None:
        self.filenames = list(sorted(glob.glob(os.path.join(base_path, "*.{}".format(suffix)))))
        self.counter = len(self.filenames)
        self.current_point = 0

    def __len__(self):
        return len(self.filenames)
    
    def __next__(self):
        self.current_point += 1
        if len(self.filenames) == 0:
            raise StopIteration
        current_filename = self.filenames.pop(0)
        im = cv2.imread(current_filename)
        return im

    def wait_stop(self, wait_time=1):
        if cv2.waitKey(wait_time)==ord('q'):
            return True
        if self.current_point == self.counter:
            return True
        else:
            return False


class VideLoader():
    def __init__(self, base_path) -> None:
        self.cap = cv2.VideoCapture(base_path)
        self.counter = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.current_point = 0
    
    def __next__(self):
        self.current_point += 1
        ret, im = self.cap.read()
        if not ret:
            StopIteration
        return im

    def wait_stop(self, wait_time=1):
        if cv2.waitKey(wait_time)==ord('q'):
            return True
        if self.current_point == self.counter:
            return True
        else:
            return False
    

class WebCamLoader(VideLoader):
    def __init__(self, cam_id=0, im_size=(1280,720)) -> None:
        super().__init__(cam_id)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, im_size[1])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, im_size[0])
        self.cap.set(cv2.CAP_PROP_FPS, 30)
    
    def wait_stop(self, wait_time=1):
        if cv2.waitKey(wait_time)==ord('q'):
            return True
        else:
            return False


if __name__ == '__main__':
    # base_path = "demo"
    # loader = ImageLoader(base_path, suffix='jpg')

    # while True:
    #     im = next(loader)
    #     """
    #     do something
    #     """
    #     cv2.imshow("", im)

    #     if loader.wait_stop():
    #         break

    # cap = VideLoader("demo.mp4")
    # while True:
    #     im = next(cap)
    #     """
    #     do something
    #     """
    #     cv2.imshow("", im)

    #     if cap.wait_stop():
    #         break

    cap = WebCamLoader(0)
    while True:
        im = next(cap)
        """
        do something
        """
        cv2.imshow("", im)

        if cap.wait_stop():
            break