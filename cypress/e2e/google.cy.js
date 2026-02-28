describe('Busca UOL', () => {
  it('Deve pesquisar algo', () => {
    cy.visit('/'); 
    cy.get('.blackBar__listProducts > :nth-child(2) > .hyperlink').contains("Bate-Papo");
         
  });
});