import React from 'react'
import styles from './styles'

type Props = {}
export const Content: React.FC<Props> = (props) => {
  return <div css={styles.content}>{props.children}</div>
}
