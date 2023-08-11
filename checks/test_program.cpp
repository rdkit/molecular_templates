#include "template_smiles.h"
#include <iostream>

int main()
{

    size_t i = 0;
    for (const auto& cxsmiles : TEMPLATE_SMILES) {
        std::cout << "Template #" << ++i << ": " << cxsmiles << std::endl;
    }

    return 0;
}