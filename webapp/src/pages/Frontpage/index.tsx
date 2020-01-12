import React, { useState } from 'react'
import styles from './styles'
import { useHistory } from 'react-router-dom'
import { Content } from 'components/Content'

type Props = {}
export const Frontpage: React.FC<Props> = () => {
  const history = useHistory()
  const [url, setUrl] = useState('')

  return (
    <div css={styles.background}>
      <Content>
        <h1>Summarizer</h1>
        <input
          type="text"
          placeholder="URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button
          onClick={() => {
            const norm = url.replace(/^https?:\/\//i, '')
            history.push(`/s/${norm}`)
          }}
        >
          Go
        </button>
      </Content>
    </div>
  )
}
