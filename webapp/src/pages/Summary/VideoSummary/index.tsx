import React, { useEffect } from 'react'
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

  let index: number = 0
  let videoPlayer: any = null

  function startSub(index: number) {
    if (!videoPlayer) {
      return
    }

    const currentTime = videoPlayer.getCurrentTime()

    const next = summary.summary[index]
    const startSeconds = next.start / 1000 - 0.25
    
    if (Math.abs(currentTime - startSeconds) > 3) {
      videoPlayer.seekTo(startSeconds, true)
    }
  }
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
          startSub(++index)
        }
      }
    }, 250)
    return () => clearInterval(interval)
  }, [])

  if (!videoId) {
    return <>Error</>
  }

  return (
    <>
      <YouTube
        videoId={videoId}
        opts={{ playerVars: { autoplay: 1, controls: 0 } }}
        onReady={({ target }) => {
          videoPlayer = target
          startSub(0)
          videoPlayer.playVideo()
        }}
      />
      {summary.summary.map((s) => (
        <p css={styles.content}>{s.text}</p>
      ))}
    </>
  )
}
