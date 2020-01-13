import React, { useState, useEffect } from 'react'
import styles from './styles'
import { useParams } from 'react-router-dom'
import { Content } from 'components/Content'

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
      summary: string[][]
      title: string
      image?: string
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
    body = 'Loading'
  } else if (data.error != null) {
    body = `${data.error}`
  } else {
    body = (
      <>
        <h1>{data.title}</h1>
        <img src={data.image || undefined} />
        {data.summary.map((p) => (
          <p css={styles.content}>{p.join(' ')}</p>
        ))}
      </>
    )
  }

  return (
    <div css={styles.page}>
      <Content>{body}</Content>
    </div>
  )
}
