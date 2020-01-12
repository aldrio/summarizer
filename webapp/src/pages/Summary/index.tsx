import React, { useState, useEffect } from 'react'
import styles from './styles'
import { useParams } from 'react-router-dom'
import { Content } from 'components/Content'

type Props = {}
export const Summary: React.FC<Props> = () => {
  const { url } = useParams()
  const [data, setData] = useState({
    loading: true,
    error: null,
    summary: null,
    title: null,
    image: null,
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
          ...data,
          loading: false,
          error: null,
        })
      } catch (error) {
        setData({
          ...data,
          loading: false,
          error: error.message,
        })
      }
    })()
  }, [])

  let body
  if (data.loading) {
    body = 'Loading'
  } else if (data.error) {
    body = `${data.error}`
  } else {
    body = (
      <>
        <h1>{data.title}</h1>
        <img src={data.image || undefined} />
        <p css={styles.content}>{data.summary}</p>
      </>
    )
  }

  return (
    <div css={styles.page}>
      <Content>{body}</Content>
    </div>
  )
}
