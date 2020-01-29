import React, { useState } from 'react'
import styles from './styles'
import { useHistory, Link } from 'react-router-dom'
import { Content } from 'components/Content'
import { Logo } from 'components/Logo'

type Props = {}
export const Frontpage: React.FC<Props> = () => {
  const history = useHistory()
  const [url, setUrl] = useState('')

  return (
    <div css={styles.background}>
      <Link to="/" css={styles.title.container}>
        <Logo width={75} height={75} /> 
        <h1 css={styles.title.text}>Summarizer</h1>
      </Link>
      <h2 css={styles.instructions}>
        Summarize an article or youtube video
      </h2>
      <Content>
        <div css={styles.search.wrapper}>
          <div
            css={styles.search.container}
            style={{
              minWidth: `${Math.min(100, 50 + url.length * 3)}%`,
            }}
          >
            <input
              type="text"
              placeholder="URL"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              css={styles.search.input}
              size={1}
            />
            <button
              css={styles.search.button}
              onClick={() => {
                const norm = url.replace(/^https?:\/\//i, '')
                history.push(`/s/${norm}`)
              }}
            >
              Summarize
            </button>
          </div>
        </div> 
      </Content>
    </div>
  )
}
