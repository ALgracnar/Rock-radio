import vlc

def stream(url):

    # define VLC instance
    instance = vlc.Instance()

    # Define VLC player
    player = instance.media_player_new()

    # Define VLC media
    media = instance.media_new(url)

    # Set player media
    player.set_media(media)

    # Play the media
    player.play()

    return player


