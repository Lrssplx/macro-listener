describe('Login Tests', () => {

  it('Login com sucesso', () => {
    cy.visit('https://www.saucedemo.com')

    cy.get('[data-test="username"]').type('standard_user')
    cy.get('[data-test="password"]').type('secret_sauce')
    cy.get('[data-test="login-button"]').click()

    cy.url().should('include', '/inventory')
  })

  it('Login inválido', () => {
    cy.visit('https://www.saucedemo.com')

    cy.get('[data-test="username"]').type('locked_out_user')
    cy.get('[data-test="password"]').type('secret_sauce')
    cy.get('[data-test="login-button"]').click()

    cy.get('[data-test="error"]').should('be.visible')
  })

})