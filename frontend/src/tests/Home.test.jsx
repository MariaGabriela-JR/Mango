import { render, screen } from '@testing-library/react'
import Home from '../app/page'

describe('Home Page', () => {
  it('renderiza o título principal', () => {
    render(<Home />)
    expect(screen.getByText('MANGO')).toBeInTheDocument()
  })

  it('tem o botão de login', () => {
    render(<Home />)
    expect(screen.getByText('Login')).toBeInTheDocument()
  })
})
