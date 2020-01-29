import { css } from '@emotion/core'
import 'utils/typography'

export default {
  content: css({
    textAlign: 'justify',
    
    transitionDuration: '0.25s',

    opacity: 0.5,

    ':hover': {
      cursor: 'pointer',
    },
  }),
  highlighted: css({
    fontWeight: 'bold',
    opacity: 1.0,
    paddingTop: 24,
    paddingBottom: 24,
  }),
}
