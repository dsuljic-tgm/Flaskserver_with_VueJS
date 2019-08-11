describe("User adden", function () {
    it("User adden", function () {
        cy.visit("http://localhost:8080/debug")
        cy.get('#__BVID__9').type("IchBinEinOger")
        cy.get('#__BVID__10').type("oger@gmx.at")
        cy.get('#__BVID__11').type("oger123")
        cy.get('#newuser').click()
        cy.get('table#usertable').within(($table) =>{
            cy.contains("IchBinEinOger")
            cy.contains("oger@gmx.at")
            cy.contains("oger123")
        })

    })

})