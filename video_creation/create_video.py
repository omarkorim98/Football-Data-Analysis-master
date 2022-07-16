import drawing.draw_frame_video as draw_frame_video
import data_statistics.voronoi_fig as voronoi_fig

from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

def video_creation():
    anim = VideoClip(lambda x: mplfig_to_npimage(draw_frame_video.draw_frame(x)[0]), duration=11)
    #Save the animation to a file
    anim.to_videofile('output/normal plotting.mp4', fps=4)
    #Display out video in 10 frame per seconds
    #anim.ipython_display(fps = 10, loop = True, autoplay = True)
    
    
def video_voronoi_creation():
    anim = VideoClip(lambda x: mplfig_to_npimage(voronoi_fig.draw_voronoi(x)[0]), duration=11)
    #Save the animation to a file
    anim.to_videofile('output/voronoi plotting.mp4', fps=4)
    #Display out videop
    #anim.ipython_display(fps = 10, loop = True, autoplay = True)