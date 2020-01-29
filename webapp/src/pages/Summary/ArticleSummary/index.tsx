import React from 'react'
import styles from './styles'
import { SummaryType } from '..'

export type Summary = {
  type: 'article'
  summary: string[][]
  image?: string
}

type Props = {
  summary: SummaryType<Summary>
}
export const ArticleSummary: React.FC<Props> = ({ summary }) => {
  return (
    <>
      <img src={summary.image || undefined} />
      {summary.summary.map((p) => (
        <p css={styles.content}>{p.join(' ')}</p>
      ))}
    </>
  )
}
