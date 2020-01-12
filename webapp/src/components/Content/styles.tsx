import { css } from '@emotion/core'
import 'utils/typography'
import mq from 'utils/mq'

export default {
  content: css({
    width: 'calc(100% - 32px)',
    marginLeft: 'auto',
    marginRight: 'auto',

    [mq[0]]: {
      width: 'calc(95% - 100px)',
      maxWidth: '30rem',
    },
  }),
}
