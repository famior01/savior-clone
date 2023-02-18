var controls = [
'play-large', // The large play button in the center
'restart', // Restart playback
'rewind', // Rewind by the seek time (default 10 seconds)
'play', // Play/pause playback
'fast-forward', // Fast forward by the seek time (default 10 seconds)
'progress', // The progress bar and scrubber for playback and buffering
'current-time', // The current time of playback
'duration', // The full duration of the media
'mute', // Toggle mute
'volume', // Volume control
//'captions', // Toggle captions
'settings', // Settings menu
'pip', // Picture-in-picture (currently Safari only)
'airplay', // Airplay (currently Safari only)
//'download', // Show a download button with a link to either the current source or a custom URL you specify in your options
'fullscreen', // Toggle fullscreen
'advertisement',
];


const player = new Plyr('#player',  {
  controls,
  ratio	: '10:5',
  loop: { active: false },
  seekTime: 10,
  disableContextMenu: true,
  tooltips: { controls: true, seek: true},
  captions	: { active: true, language: 'en', update: true },

  /*ads: {
    enabled: true,
    publisherId: '',
    tagUrl: '' ,
  },

  mediaMetadata: {
    title: '{{ IWatch.title }}',
    artist: '{{ IWatch.creator.user.full_name }}',
    album: '',
  },*/
});
player.source = {
  type: 'video',
  title: '',
  /*sources: [
      { 
        src: '{{ IWatch.video.url }}',
        type: 'video/mp4',
        size: 720,
      }, 
      {
        src: '{{ IWatch.video.url }}',
        type: 'video/webm',
        size: 1080,
      },
    ],
  poster: '{{ IWatch.thumbnail.url }} ',
  previewThumbnails: {
    src: '{{ IWatch.thumbnail.url }}',
  },
  tracks: [
    {
      kind: 'captions',
      label: 'English',
      srclang: 'en',
      //src: '/path/to/captions.en.vtt',
      default: true,
    },
    {
      kind: 'captions',
      label: 'Urdu',
      srclang: 'ur',
      //src: '/path/to/captions.ur.vtt',
    }, 
  ],*/
};

// player.on('seeking', (event) => {
//   //increase seeking time
//   player.currentTime += 10;
// });

// player.rewind(4);
// player.forward(4); {% endcomment %}

// {% comment %} var adPlayer = plyr.setup();
// plyrAds.setup(adPlayer, {
//   adTagUrl: 'https://savior-staticfiles.sgp1.cdn.digitaloceanspaces.com/media%2Fzakat_video%2Fangry.mp4',
// }); 


// ==========================================================================
// =====================       For Zakat Videos             =======================
// ==========================================================================


var Zcontrols = [
  'play-large', // The large play button in the center
  //'restart', // Restart playback
  //'rewind', // Rewind by the seek time (default 10 seconds)
  'play', // Play/pause playback
  //'fast-forward', // Fast forward by the seek time (default 10 seconds)
  'progress', // The progress bar and scrubber for playback and buffering
  'current-time', // The current time of playback
  'duration', // The full duration of the media
  'mute', // Toggle mute
  'volume', // Volume control
  //'captions', // Toggle captions
  'settings', // Settings menu
  'pip', // Picture-in-picture (currently Safari only)
  //'airplay', // Airplay (currently Safari only)
  //'download', // Show a download button with a link to either the current source or a custom URL you specify in your options
  'fullscreen', // Toggle fullscreen
  //'advertisement',
  ];
const zakatvidoes = new Plyr('#zakat1',  {
  Zcontrols,
  ratio	: '9:5',
  loop: { active: false },
  seekTime: 10,
  disableContextMenu: true,
  tooltips: { controls: true, seek: true},
  captions	: { active: true, language: 'en', update: true },
});
zakatvidoes.source = {
  type: 'video',
  title: '',
};

const zakatvidoes2 = new Plyr('#zakat2',  {
  Zcontrols,
  ratio	: '9:5',
  loop: { active: false },
  seekTime: 10,
  disableContextMenu: true,
  tooltips: { controls: true, seek: true},
  captions	: { active: true, language: 'en', update: true },
});
zakatvidoes2.source = {
  type: 'video',
  title: '',
};
