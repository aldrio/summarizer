import { css } from '@emotion/core'
import 'utils/typography'

export default {
  page: css({
    minHeight: '100vh',
    display: 'flex',
    backgroundColor: '#fff',
    flexDirection: 'row',
    paddingTop: 100,
    paddingBottom: 100,
  }),

  content: css({
    textAlign: 'justify',
  }),
}
