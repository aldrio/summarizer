import { css } from '@emotion/core'
import 'utils/typography'

export default {
  page: css({
    minHeight: '100vh',
    display: 'flex',
    backgroundColor: '#fff',
    flexDirection: 'row',
    paddingTop: 76,
    paddingBottom: 100,
  }),

  content: css({
    textAlign: 'justify',
  }),

  info: css({
    marginBottom: '2rem',
  }),

  urlLink: css({
    display: 'inline-flex',
    alignItems: 'center',

    textDecoration: 'none',
    color: '#6F6F93',
    transitionDuration: '0.125s',
    ':hover': {
      color: '#373657',
    },
  }),

  icon: css({
    margin: 0,
    padding: 0,
    display: 'inline',
    height: '1.25rem',
    width: '1.25rem',
  }),
  
  domain: css({
    display: 'inline',
    fontWeight: 'bold',
    paddingLeft: 12,
    paddingRight: 8,
  }),
}
