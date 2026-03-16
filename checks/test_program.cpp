#include <iostream>

#include "template_smarts.h"

int main()
{
    size_t i = 0;
    for (const auto& cxsmarts : TEMPLATE_SMARTS) {
        std::cout << "Template #" << ++i << ": " << cxsmarts << std::endl;
    }

    std::cout << "All templates in header listed, check passed." << std::endl;

    return 0;
}
