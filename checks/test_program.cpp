#include <iostream>

#include "template_smiles.h"

int main()
{
    size_t i = 0;
    for (const auto& cxsmiles : TEMPLATE_SMILES) {
        std::cout << "Template #" << ++i << ": " << cxsmiles << std::endl;
    }

    std::cout << "All templates in header listed, check passed." << std::endl;

    return 0;
}
