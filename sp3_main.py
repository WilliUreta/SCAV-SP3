import os
import subprocess


def resize_vid(path, output_size):

    if output_size==1:
        actual_size = str("scale=720:480")
        output_name = "720_480_original.mp4"
    elif output_size==2:
        actual_size = str("scale=480:360")
        output_name = "480_360_original.mp4"
    elif output_size == 3:
        actual_size = str("scale=360:240")
        output_name = "360_240_original.mp4"
    elif output_size == 4:
        actual_size = str("scale=160:120")
        output_name = "160_120_original.mp4"
    else:
        print("No  valid resolution")
        return

    subprocess.call(["ffmpeg", "-i", path, "-vf", actual_size, output_name])
    return output_name


def convert_2_codecs(path, output_size, output_name):

    # Resize original video
    temporal_output_name = resize_vid(path, output_size)

    # Convert into all video codecs codecs

    # VP8   ffmpeg -i cut_BBB.mp4 -c:v libvpx -crf 10 -b:v 2.5M test_vp8.webm
    # 2.5 based on the original bitrate of the h264 vid

    subprocess.call(["ffmpeg", "-i", temporal_output_name, "-c:v",
                     "libvpx", "-crf", "30", "-b:v", "1.5M", (output_name+"_vp8.webm")])

    # VP9   ffmpeg -i cut_BBB.mp4 -c:v libvpx-vp9 -crf 10 -b:v 2.5M test_vp8.webm
    # ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 2M -pass 1 -an -f null /dev/null && \
    # ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 2M -pass 2 -c:a libopus output.webm

    subprocess.call(["ffmpeg", "-i", temporal_output_name, "-c:v",
                     "libvpx-vp9", "-b:v", "0", "-crf", "40", "-pass","1", "-an",
                     "-f", "null", "/dev/null"])

    subprocess.call(["ffmpeg", "-i",
                     temporal_output_name, "-c:v", "libvpx-vp9", "-b:v", "0",
                     "-crf", "40", "-pass", "2", "-c:a", "libopus", (output_name+"_vp9.webm")])

    # H265 2-pass no va, 1pass: ffmpeg -i 4s_BBB.mp4 -c:v libx265 -crf 30 -preset fast -c:a copy h265output.mp4
    subprocess.call(["ffmpeg", "-i", temporal_output_name, "-c:v", "libx265", "-crf",
                     "30", "-preset", "medium", "-c:a", "copy",
                     (output_name + "_h265.mp4")])

    # AV1 -cpu-used 1 + lent, moooolt important: ffmpeg -i 4s_BBB.mp4 -c:v libaom-av1 -cpu-used 3 -crf 50 -b:v 0 av1_test2.mkv
    subprocess.call(["ffmpeg", "-i", temporal_output_name, "-c:v", "libaom-av1",
                     "-cpu-used", "3", "-crf", "40", "-preset", "medium",
                     "-c:a", "copy", (output_name + "_av1.mkv")])

    if os.path.exists(temporal_output_name):
        os.remove(temporal_output_name)


def comparison_stack(path, option, output_name):

    if option == 1: #VP8 vs vp9
        video1 = "temp_vp8.webm"
        video2 = "temp_vp9.webm"
        subprocess.call(["ffmpeg", "-i", path, "-c:v",
                         "libvpx", "-crf", "40", "-b:v", "1.5M",
                         video1])

        subprocess.call(["ffmpeg", "-i", path, "-c:v",
                         "libvpx-vp9", "-b:v", "0", "-crf", "40", "-pass", "1",
                         "-an",
                         "-f", "null", "/dev/null"])
        # Funciona pero crec que esta malament
        subprocess.call(["ffmpeg", "-i",
                         path, "-c:v", "libvpx-vp9", "-b:v",
                         "0",
                         "-crf", "40", "-pass", "2", "-c:a", "libopus",
                         video2])
    elif option == 2:   #VP8 vs h265
        video1 = "temp_vp8.webm"
        video2 = "temp_h265.mp4"
        subprocess.call(["ffmpeg", "-i", path, "-c:v",
                         "libvpx", "-crf", "40", "-b:v", "1.5M",
                         video1])

        subprocess.call(["ffmpeg", "-i", path, "-c:v", "libx265", "-crf",
             "30", "-preset", "medium", "-c:a", "copy",
             video2])

    elif option == 3:   #VP8 vs AV1
        video1 = "temp_vp8.webm"
        video2 = "temp_av1.mkv"
        subprocess.call(["ffmpeg", "-i", path, "-c:v",
                         "libvpx", "-crf", "30", "-b:v", "1.5M",
                         video1])

        subprocess.call(["ffmpeg", "-i", path, "-c:v", "libaom-av1",
             "-cpu-used", "3", "-crf", "40", "-preset", "medium",
             "-c:a", "copy", video2])
    elif option == 4:   # VP9 vs H265
        video1 = "temp_vp9.webm"
        video2 = "temp_h265.mp4"
        subprocess.call(["ffmpeg", "-i", path, "-c:v",
                         "libvpx-vp9", "-b:v", "0", "-crf", "30", "-pass", "1",
                         "-an",
                         "-f", "null", "/dev/null"])
        # Funciona pero crec que esta malament
        subprocess.call(["ffmpeg", "-i",
                         path, "-c:v", "libvpx-vp9", "-b:v","0", "-crf", "40",
                         "-pass", "2", "-c:a", "libopus", video1])

        subprocess.call(["ffmpeg", "-i", path, "-c:v", "libx265", "-crf",
             "40", "-preset", "medium", "-c:a", "copy", video2])
    elif option == 5:   # VP9 vs AV1
        video1 = "temp_vp9.webm"
        video2 = "temp_av1.mkv"
        subprocess.call(["ffmpeg", "-i", path, "-c:v",
                         "libvpx-vp9", "-b:v", "0", "-crf", "40", "-pass", "1",
                         "-an",
                         "-f", "null", "/dev/null"])
        # Funciona pero crec que esta malament
        subprocess.call(["ffmpeg", "-i",
                         path, "-c:v", "libvpx-vp9", "-b:v",
                         "0", "-crf", "40", "-pass", "2", "-c:a", "libopus",
                         video1])

        subprocess.call(["ffmpeg", "-i", path, "-c:v", "libaom-av1",
             "-cpu-used", "3", "-crf", "40", "-preset", "medium",
             "-c:a", "copy", video2])
    elif option == 6:   # H265 vs AV1
        video1 = "temp_h265.mp4"
        video2 = "temp_av1.mkv"
        subprocess.call(["ffmpeg", "-i", path, "-c:v", "libx265", "-crf",
                         "30", "-preset", "medium", "-c:a", "copy",
                         video1])

        subprocess.call(["ffmpeg", "-i", path, "-c:v", "libaom-av1",
                         "-cpu-used", "3", "-crf", "40", "-preset", "medium",
                         "-c:a", "copy", video2])
    else:
        print("Option not valid")
        return

# ffmpeg -i input0 -i input1 -filter_complex "[0:v][1:v]vstack=inputs=2[v];[0:a][1:a]amerge=inputs=2[a]" -map "[v]" -map "[a]" -ac 2 output
# "\"[0:v][1:v]vstack=inputs=2[v];[0:a][1:a]amerge=inputs=2[a]\"",
    subprocess.call(["ffmpeg", "-i", video1, "-i", video2, "-filter_complex",
                     "[0:v][1:v]vstack=inputs=2[v];[0:a][1:a]amerge=inputs=2[a]",
                     "-map", "[v]", "-map", "[a]", "-ac", "2", (output_name+".mp4")])
    # https://stackoverflow.com/questions/17623676/text-on-video-ffmpeg

    if os.path.exists(video1):
        os.remove(video1)
    if os.path.exists(video2):
        os.remove(video2)

    #Don't have --enable-libfreetype, --enable-libfontconfig enabled during compile.
    print("The top video will always be the first codec when you choose. "
          "\nEx: VP8 vs H265, Top video is VP8 and bottom is H265")


def broadcast_video(path,ip):

     # https://trac.ffmpeg.org/wiki/StreamingGuide
    # https://stackoverflow.com/questions/26999595/what-steps-are-needed-to-stream-rtsp-from-ffmpeg
    # https://newbedev.com/what-steps-are-needed-to-stream-rtsp-from-ffmpeg
    # use -re to read from file at native framerate
    # ffmpeg -re -i BBB.mp4 -v 0 -vcodec mpeg4 -f mpegts udp://127.0.0.1:23000
    # ffmpeg -re -i BBB.mp4 -v 0 -f mpegts udp://127.0.0.1:23000    Va be!, es veu una mica xungo.
    # -v 0 to set logs to 0, menys spam
    # ffmpeg -re -i BBB.mp4 -v 0 -c:v copy -f mpegts udp://127.0.0.1:23000
    # ffplay udp://127.0.0.1:23000
    final_ip = "udp://"+ip
    print("If you don't see any more message, check in VLC for udp://@:<your_port>")
    subprocess.call(["ffmpeg", "-re", "-i", path, "-v", "0",
                     "-c:v", "copy", "-f", "mpegts", final_ip])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
    program = int(input("Choose what program to run: \n1. Convert to VP8, VP9 h265 & AV1"
                        "\n2. Generate Video comparison of 2 codecs "
                        "\n3. Broadcast to selected IP\n"))

    if program == 1:
        path = input("Enter path to video file you want to cut: ")
        output_size = int(input("\nChoose output resolution:\n1. 720p"
                       "\n2. 480p \n3. 360x240 \n4. 160x120 \n"))
        output_name = input("Name of output file (without extension): ")
        convert_2_codecs(path, output_size, output_name)
    elif program == 2:
        path = input("Enter path to video file you want to compare 2 codecs: ")
        option = int(input("\nWhich combination of 2 codecs do you want:\n1. VP8 vs VP9 "
                     "\n2. VP8 vs H265 \n3. VP8 vs AV1 \n4. VP9 vs H265 "
                     "\n5. VP9 vs AV1 \n6. H265 vs AV1\n"))
        output_name = input("\nName of output file (without extension): ")
        comparison_stack(path,option,output_name)
    elif program == 3:
        path = input("Enter path to video file you want to broadcast: ")
        ip = input("Choose the IP and port (127.0.0.1:1234):"
                       "\nFor local playback we recommend the example IP\n")
        broadcast_video(path, ip)

    else:
        print("Program not valid")