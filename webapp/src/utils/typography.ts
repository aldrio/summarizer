import Typography from 'typography'
import 'typeface-open-sans'

const typography = new Typography({
  baseFontSize: '20px',
  baseLineHeight: 1.666,
  headerFontFamily: ['Open Sans', 'sans-serif'],
  bodyFontFamily: ['Open Sans', 'sans-serif'],
})

typography.injectStyles()
