import { css } from '@emotion/core'
import 'utils/typography'

export default {
  page: css({
    minHeight: '100vh',
    display: 'flex',
    backgroundColor: '#fff',
    flexDirection: 'row',
    paddingBottom: 100,
  }),

  header: css({
    textAlign: 'center',
    marginBottom: 70,
  }),

  brand: {
    container: css({
      textDecoration: 'none',
      display: 'inline-flex',
      alignItems: 'center',
      marginTop: 12,
    }),
    text: css({
      margin: 0,
      marginLeft: 8,
      fontSize: '1rem',
      color: '#373657',
    })
  },

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

  loading: css({
    display: 'flex',
    paddingTop: '20vh',
    paddingBottom: '20vh',
    justifyContent: 'center',
    alignItems: 'center',
  }),
}
