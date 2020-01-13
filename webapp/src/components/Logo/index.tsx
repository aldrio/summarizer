import React from 'react'
import styles from './styles'
import { ReactComponent as LogoSvg } from './logo.svg';

type Props = {} | React.SVGProps<SVGSVGElement>
export const Logo: React.FC<Props> = (props) => {
  return <LogoSvg {...props} />
}
