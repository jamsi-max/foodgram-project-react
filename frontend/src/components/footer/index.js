import styles from './style.module.css'
import { Container, LinkComponent } from '../index'

const Footer = () => {
  return <footer className={styles.footer}>
      <Container className={styles.footer__container}>
        <LinkComponent href='#' title='Продуктовый помощник Foodgram © Сopyright by @jony2024(telegram)' className={styles.footer__brand} />
      </Container>
  </footer>
}

export default Footer
