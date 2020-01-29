import React, { useEffect, useState } from 'react'
import styles from './styles'
import { SummaryType } from '..'
import YouTube from 'react-youtube'

export type Summary = {
  type: 'video'
  summary: {
    text: string
    start: number
    end: number
  }[]
}

type Props = {
  summary: SummaryType<Summary>
}
export const VideoSummary: React.FC<Props> = ({ summary }) => {
  const match = summary.url.match(/(.*(\/|v=))(.+)$/)
  const videoId = match?.[3]

  let [index, setIndex] = useState(0)
  let [videoPlayer, setVideoPlayer] = useState<any>(null)

  // Change to correct time when index changes
  useEffect(() => {
    if (!videoPlayer) {
      return
    }

    const currentTime = videoPlayer.getCurrentTime()

    const next = summary.summary[index]
    const startSeconds = next.start / 1000 - 0.25

    if (Math.abs(currentTime - startSeconds) > 3) {
      videoPlayer.seekTo(startSeconds, true)
    }
  }, [videoPlayer, index])

  // Set an interval to poll if the index should change
  useEffect(() => {
    const interval = setInterval(() => {
      if (!videoPlayer) {
        return
      }
      const currentTime = videoPlayer.getCurrentTime()
      const current = summary.summary[index]
      const endSeconds = current.end / 1000 + 0.25

      if (currentTime > endSeconds) {
        if (summary.summary.length - 1 == index) {
          videoPlayer.stopVideo()
        } else {
          setIndex(index + 1)
        }
      }
    }, 250)
    return () => clearInterval(interval)
  }, [index, videoPlayer])

  if (!videoId) {
    return <>Error</>
  }

  return (
    <>
      <YouTube
        videoId={videoId}
        opts={{ playerVars: { autoplay: 1, controls: 0 }, width: '100%' }}
        onReady={({ target }) => {
          setVideoPlayer(target)
        }}
      />
      {summary.summary.map((s, id) => (
        <p
          key={id}
          onClick={() => setIndex(id)}
          css={[styles.content, index == id && styles.highlighted]}
        >
          {s.text}
        </p>
      ))}
    </>
  )
}
