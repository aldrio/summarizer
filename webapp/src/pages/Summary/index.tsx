import React, { useState, useEffect } from 'react'
import styles from './styles'
import { useParams, Link } from 'react-router-dom'
import { Content } from 'components/Content'
import { HashLoader } from 'react-spinners'
import FadeIn from 'react-fade-in'

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

      url: string
      title: string
      summary: string[][]
      image?: string
      icon: string
    }
type Props = {}
export const Summary: React.FC<Props> = () => {
  const { url } = useParams()
  const [data, setData] = useState<Data>({
    loading: true,
  })

  // Query url from api
  useEffect(() => {
    ;(async () => {
      try {
        const res = await fetch(
          `http://localhost:8000/summarize?url=${encodeURIComponent(
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
          ...data,
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
    body = (
      <FadeIn>
        <div css={styles.info}>
          <a css={styles.urlLink} href={data.url}>
            <img src={data.icon} css={styles.icon} />
            <span css={styles.domain}>
              {new URL(data.url).hostname.replace(/^www\./i, '')}
            </span>
          </a>
        </div>
        <h1>{data.title}</h1>
        <img src={data.image || undefined} />
        {data.summary.map((p) => (
          <p css={styles.content}>{p.join(' ')}</p>
        ))}
      </FadeIn>
    )
  }

  return (
    <div css={styles.page}>
      <Content>
        <div css={styles.header}>
          <h1>
            <Link to="/" css={styles.brand}>
              Text Summarizer
            </Link>
          </h1>
        </div>
        {body}
      </Content>
    </div>
  )
}
