import React, { useState, useEffect } from 'react'
import styles from './styles'
import { useParams, Link, useLocation } from 'react-router-dom'
import { Content } from 'components/Content'
import { HashLoader } from 'react-spinners'
import FadeIn from 'react-fade-in'
import { Logo } from 'components/Logo'
import { ArticleSummary, Summary as ArticleSummaryType } from './ArticleSummary'
import { VideoSummary, Summary as VideoSummaryType } from './VideoSummary'

export type SummaryType<T> = {
  url: string
  title: string
  icon: string
} & T

type Data =
  | {
      loading: true
    }
  | {
      loading: false
      error: string
    }
  | {
      loading: false
      error: null
      summary: SummaryType<ArticleSummaryType> | SummaryType<VideoSummaryType>
    }

type Props = {}
export const Summary: React.FC<Props> = () => {
  const [data, setData] = useState<Data>({
    loading: true,
  })

  const { search: queryString } = useLocation()
  let { url } = useParams()
  url += queryString

  // Query url from api
  useEffect(() => {
    ;(async () => {
      try {
        const res = await fetch(
          `${process.env.REACT_APP_API_URL}?url=${encodeURIComponent(
            (url || '').toString()
          )}`
        )
        if (!res.ok) {
          throw new Error('Error summarizing page')
        }
        const data = await res.json()
        setData({
          loading: false,
          error: null,
          summary: data,
        })
      } catch (error) {
        setData({
          loading: false,
          error: error.message,
        })
      }
    })()
  }, [])

  let body
  if (data.loading) {
    body = (
      <div css={styles.loading}>
        <FadeIn>
          <HashLoader size={100} color="#6F6F93" />
        </FadeIn>
      </div>
    )
  } else if (data.error != null) {
    body = `${data.error}`
  } else {
    const { summary } = data
    let renderedSummary
    if (summary.type == 'article') {
      renderedSummary = <ArticleSummary summary={summary} />
    } else if (summary.type == 'video') {
      renderedSummary = <VideoSummary summary={summary} />
    }

    body = (
      <FadeIn>
        <div css={styles.info}>
          <a css={styles.urlLink} href={summary.url}>
            <img src={summary.icon} css={styles.icon} />
            <span css={styles.domain}>
              {new URL(summary.url).hostname.replace(/^www\./i, '')}
            </span>
          </a>
        </div>
        <h1>{summary.title}</h1>
        {renderedSummary}
      </FadeIn>
    )
  }

  return (
    <div css={styles.page}>
      <Content>
        <div css={styles.header}>
          <Link to="/" css={styles.brand.container}>
            <Logo width={'1rem'} height={'1rem'} />
            <h1 css={styles.brand.text}>Summarizer</h1>
          </Link>
        </div>
        {body}
      </Content>
    </div>
  )
}
