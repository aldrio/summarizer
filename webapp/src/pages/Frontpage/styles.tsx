import { css } from '@emotion/core'
import 'utils/typography'

export default {
  background: css({
    minHeight: '100vh',
    display: 'flex',
    backgroundColor: '#fff',
    paddingTop: 12,
    paddingBottom: 100,
    
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  }),

  content: css({
    height: '100%',
    width: '100%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  }),

  title: css({
    textAlign: 'center',
    fontSize: '3rem',
    marginBottom: '2.5rem',
  }),

  search: {
    wrapper: css({
      display: 'flex',
      flexDirection: 'row',
      justifyContent: 'center',
    }),
    container: css({
      display: 'inline-flex',
      transitionDuration: '0.2s',
    }),
    input: css({
      flexGrow: 1,
      minWidth: 187,
      padding: 10,
      borderRadius: 2,
      border: 'none',
      borderStyle: 'solid',
      borderWidth: 2,
      borderColor: '#6F6F93',
    }),
    button: css({
      marginLeft: 8,
      border: 'none',
      backgroundColor: '#6F6F93',
      fontWeight: 'bold',
      color: 'white',
      borderRadius: 2,
      padding: 10,
    }),
  },
}
